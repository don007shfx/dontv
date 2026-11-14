"""The opt-in tweaks (frame-rate matching, quiet home), the VPN check that keeps the DNS
filter away from Proton VPN and the like, and the read-only health readout, against a
pretend Fire TV.

Run: python3 -m unittest discover -s tests -v
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WRITES = ("settings put", "settings delete", "pm disable", "pm enable", "pm uninstall",
          "appops set", "cmd netpolicy", "am force-stop", "device_config put", "reboot",
          "svc power")


class FakeTv:
    def __init__(self, tmp, packages=None, settings=None, conf="", sdk=30, **extra):
        self.tmp = Path(tmp)
        self.state = self.tmp / "state.json"
        self.state.write_text(json.dumps({"packages": packages or {}, "settings": settings or {},
                                          "sdk": sdk, **extra}))
        self.log = self.tmp / "commands.log"
        self.log.touch()
        self.conf = self.tmp / "dumbtv.conf"
        self.conf.write_text(conf)
        self.report = self.tmp / "report"

    def run(self, script, *flags):
        env = dict(os.environ, ADB=str(ROOT / "tests" / "fake_tv.py"), ADB_SERIAL="test-tv:5555",
                   FAKE_TV_STATE=str(self.state), FAKE_TV_LOG=str(self.log), CONF=str(self.conf),
                   REPORT=str(self.report), BOOT_SECONDS="0", PM_WRITE_SECONDS="0")
        for k in ("FRAMERATE", "QUIET_HOME", "HOME_APP", "LAUNCHER", "DNSFILTER", "ALEXA"):
            env.pop(k, None)
        return subprocess.run(["bash", str(ROOT / "scripts" / f"{script}.sh"), *flags],
                              env=env, capture_output=True, text=True, timeout=180)

    @property
    def settings(self):
        return json.loads(self.state.read_text())["settings"]

    @property
    def commands(self):
        return self.log.read_text().splitlines()


class OptInTweaksTest(unittest.TestCase):
    def test_off_by_default_and_never_touched(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, settings={"global/match_content_frame_rate": "0"})
            result = tv.run("debloat", "-y", "--no-reboot")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(tv.settings["global/match_content_frame_rate"], "0")
            self.assertFalse(any("match_content_frame_rate" in c and c.startswith("settings put")
                                 for c in tv.commands))
            self.assertFalse(any("auto_play_" in c and c.startswith("settings put") for c in tv.commands))

    def test_framerate_on_then_off_puts_the_tv_value_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, conf="FRAMERATE=1\n")
            result = tv.run("debloat", "-y", "--no-reboot")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(tv.settings["global/match_content_frame_rate"], "1")
            self.assertEqual(tv.settings["global/dumbtv_was_match_content_frame_rate"], "unset")
            # A second run must not record its own value as the original.
            tv.run("debloat", "-y", "--no-reboot")
            self.assertEqual(tv.settings["global/dumbtv_was_match_content_frame_rate"], "unset")
            tv.conf.write_text("FRAMERATE=0\n")
            result = tv.run("debloat", "-y", "--no-reboot")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("global/match_content_frame_rate", tv.settings)
            self.assertNotIn("global/dumbtv_was_match_content_frame_rate", tv.settings)

    def test_restore_puts_back_an_earlier_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, conf="QUIET_HOME=1\n", settings={"global/auto_play_video": "2"})
            tv.run("debloat", "-y", "--no-reboot")
            self.assertEqual(tv.settings["global/auto_play_video"], "0")
            self.assertEqual(tv.settings["global/auto_play_audio"], "0")
            # restore.sh undoes it whatever dumbtv.conf says now.
            tv.conf.write_text("")
            result = tv.run("restore", "-y")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(tv.settings["global/auto_play_video"], "2")
            self.assertNotIn("global/auto_play_audio", tv.settings)
            self.assertFalse(any(k.split("/")[1].startswith("dumbtv_was_") for k in tv.settings))

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, conf="FRAMERATE=1\nQUIET_HOME=1\n")
            result = tv.run("debloat", "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("match_content_frame_rate", result.stdout + result.stderr)
            self.assertEqual(tv.settings, {})

    def test_configure_records_the_tweaks(self):
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "dumbtv.conf"
            result = subprocess.run(
                ["bash", str(ROOT / "scripts" / "configure.sh"), "-y", "--framerate", "1"],
                env=dict(os.environ, CONF=str(conf)), capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("FRAMERATE=1", conf.read_text())
            self.assertIn("QUIET_HOME=0", conf.read_text())


class VpnConflictTest(unittest.TestCase):
    PROTON = {"ch.protonvpn.android": {"system": False, "enabled": True}}

    def test_dnsfilter_steps_aside_for_proton_vpn(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, packages=self.PROTON)
            result = tv.run("dnsfilter", "-y")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Proton VPN", result.stderr)
            self.assertFalse(any(c.startswith(WRITES) for c in tv.commands), tv.commands)
            self.assertNotIn("secure/always_on_vpn_app", tv.settings)

    def test_any_always_on_vpn_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, settings={"secure/always_on_vpn_app": "com.example.vpn"})
            result = tv.run("dnsfilter", "-y")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("com.example.vpn", result.stderr)
            self.assertEqual(tv.settings["secure/always_on_vpn_app"], "com.example.vpn")

    def test_preflight_says_the_filter_will_be_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, packages=self.PROTON)
            result = tv.run("preflight", "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("skip the DNS filter: ch.protonvpn.android", result.stderr)


class HealthTest(unittest.TestCase):
    def test_reports_what_an_update_switched_back_on_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp, packages={
                "com.amazon.tv.acr": {"system": True, "enabled": True},
                "com.amazon.hedwig": {"system": True, "enabled": False},
                "ch.protonvpn.android": {"system": False, "enabled": True},
                "com.spocky.projengmenu": {"system": False, "enabled": True}})
            tv.report.mkdir()
            (tv.report / "debloat.txt").write_text(
                "com.amazon.tv.acr\tdisabled\ncom.amazon.hedwig\tdisabled\n")
            result = tv.run("health")
            out = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, out)
            self.assertIn("enabled again  com.amazon.tv.acr", out)
            self.assertNotIn("com.amazon.hedwig", out.split("enabled again")[1].splitlines()[0])
            self.assertIn("other vpn", out)
            self.assertIn("not exempt from doze", out)
            self.assertIn("something above needs attention", out)
            self.assertFalse(any(c.startswith(WRITES) for c in tv.commands), tv.commands)

    def test_flags_are_the_shared_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            tv = FakeTv(tmp)
            result = tv.run("health", "--bogus")
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
