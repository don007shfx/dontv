"""repair.sh against a pretend Fire TV that an update partly undid: it puts back only
what drifted, asks first, and changes nothing on a dry run.

Run: python3 -m unittest discover -s tests -v
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "fireos"


def entries(path):
    out = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line.split()[0])
    return out


def settings_wanted():
    out = {}
    for line in (DATA / "settings.txt").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            ns, key, value = line.replace(" = ", " ").split(None, 2)
            out[f"{ns}/{key}"] = value
    return out


CLEANUP = entries(DATA / "packages.txt")
PROTECTED = entries(DATA / "protected.txt")
SERIAL = "G4N0TEST"


class RepairTest(unittest.TestCase):
    def run_repair(self, *flags, drop=(), settings=None, extra=None, record=True, conf="",
                   saver=False, blacklist=None, answer=None, lockdown_record=False):
        """A TV debloated by the last pass, then partly undone: packages in `drop` are on
        again and `settings` overrides what the pass set."""
        packages = {p: {"system": True, "enabled": p in drop} for p in CLEANUP}
        packages.update(extra or {})
        live = settings_wanted()
        live.update(settings or {})
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            state = tmp / "state.json"
            state.write_text(json.dumps({"packages": packages, "settings": live,
                                         "props": {"ro.serialno": SERIAL}, "saver": saver,
                                         "blacklist": blacklist or []}))
            report = tmp / "report"
            report.mkdir()
            if record:
                (report / "debloat.txt").write_text(
                    f"#device\t{SERIAL}\n" + "".join(f"{p}\tdisabled\n" for p in CLEANUP))
            if lockdown_record:
                (report / "lockdown.txt").write_text(f"#device\t{SERIAL}\n")
            log = tmp / "commands.log"
            log.touch()
            (tmp / "dumbtv.conf").write_text(conf)
            env = dict(os.environ, ADB=str(ROOT / "tests" / "fake_tv.py"), ADB_SERIAL="test-tv",
                       FAKE_TV_STATE=str(state), FAKE_TV_LOG=str(log), CONF=str(tmp / "dumbtv.conf"),
                       REPORT=str(report))
            for k in ("REMOVE_EXTRA", "KEEP_APPS", "ALEXA", "DNSFILTER"):
                env.pop(k, None)
            result = subprocess.run(["bash", str(ROOT / "scripts" / "repair.sh"), *flags],
                                    env=env, capture_output=True, text=True, timeout=300,
                                    input=answer)
            self.output = result.stdout + result.stderr
            self.commands = log.read_text().splitlines()
            return result, json.loads(state.read_text())

    def changes(self):
        return [c for c in self.commands if c.startswith(
            ("pm disable-user", "pm enable", "settings put", "settings delete", "cmd netpolicy add",
             "cmd netpolicy set", "appops set", "am force-stop"))]

    def test_nothing_drifted_means_nothing_to_do(self):
        result, _ = self.run_repair("-y")
        self.assertEqual(result.returncode, 0, self.output)
        self.assertIn("nothing drifted", self.output)
        self.assertEqual(self.changes(), [])

    def test_only_the_packages_an_update_switched_on_are_disabled_again(self):
        back = CLEANUP[:2]
        result, state = self.run_repair("-y", drop=back)
        self.assertEqual(result.returncode, 0, self.output)
        disabled = [c.split()[-1] for c in self.commands if c.startswith("pm disable-user")]
        self.assertEqual(sorted(disabled), sorted(back))
        for p in back:
            self.assertFalse(state["packages"][p]["enabled"])

    def test_a_package_someone_else_turned_on_outside_the_record_is_left(self):
        # The record names only what the last pass disabled; with it, nothing else is touched.
        extra = {"com.amazon.cloud9": {"system": True, "enabled": True}}
        result, _ = self.run_repair("-y", extra=extra)
        self.assertEqual(result.returncode, 0, self.output)
        self.assertNotIn("pm disable-user --user 0 com.amazon.cloud9", self.commands)

    def test_drifted_settings_are_put_back_and_the_rest_left(self):
        result, state = self.run_repair("-y", settings={"secure/limit_ad_tracking": "0"})
        self.assertEqual(result.returncode, 0, self.output)
        puts = [c for c in self.commands if c.startswith("settings put")]
        self.assertEqual(puts, ["settings put secure limit_ad_tracking 1"])
        self.assertEqual(state["settings"]["secure/limit_ad_tracking"], "1")

    def test_dry_run_changes_nothing(self):
        result, state = self.run_repair("--dry-run", drop=CLEANUP[:1],
                                        settings={"secure/limit_ad_tracking": "0"})
        self.assertEqual(result.returncode, 0, self.output)
        self.assertEqual(self.changes(), [])
        self.assertTrue(state["packages"][CLEANUP[0]]["enabled"])
        self.assertIn("dry-run: nothing was changed", self.output)

    def test_it_asks_first_and_no_means_no(self):
        result, state = self.run_repair(drop=CLEANUP[:1], answer="n\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cancelled", self.output)
        self.assertEqual(self.changes(), [])

    def test_the_boot_guard_also_holds_here(self):
        victim = CLEANUP[0]
        result, _ = self.run_repair("-y", extra={victim: {"system": True, "enabled": True,
                                                          "persistent": True}})
        self.assertEqual(result.returncode, 0, self.output)
        self.assertNotIn(f"pm disable-user --user 0 {victim}", self.commands)

    def test_the_dns_filter_gets_its_vpn_slot_back(self):
        extra = {"dnsfilter.android": {"system": False, "enabled": True}}
        result, state = self.run_repair("-y", extra=extra)
        self.assertEqual(result.returncode, 0, self.output)
        self.assertEqual(state["settings"]["secure/always_on_vpn_app"], "dnsfilter.android")

    def test_another_vpn_app_keeps_the_slot(self):
        extra = {"dnsfilter.android": {"system": False, "enabled": True},
                 "ch.protonvpn.android": {"system": False, "enabled": True}}
        result, state = self.run_repair("-y", extra=extra)
        self.assertEqual(result.returncode, 0, self.output)
        self.assertNotIn("secure/always_on_vpn_app", state["settings"])
        self.assertIn("ch.protonvpn.android holds the VPN slot", self.output)

    def test_no_dns_filter_set_up_means_none_touched(self):
        extra = {"dnsfilter.android": {"system": False, "enabled": True}}
        result, state = self.run_repair("-y", extra=extra, conf="DNSFILTER=0\n")
        self.assertEqual(result.returncode, 0, self.output)
        self.assertNotIn("secure/always_on_vpn_app", state["settings"])

    def test_the_lockdown_comes_back_when_it_was_set_up(self):
        extra = {PROTECTED[0]: {"system": True, "enabled": True}}
        result, state = self.run_repair("-y", extra=extra, saver=False, lockdown_record=True)
        self.assertEqual(result.returncode, 0, self.output)
        self.assertTrue(state["saver"])
        self.assertIn(10050, state["blacklist"])

    def test_no_lockdown_set_up_means_none_applied(self):
        extra = {PROTECTED[0]: {"system": True, "enabled": True}}
        result, state = self.run_repair("-y", extra=extra)
        self.assertEqual(result.returncode, 0, self.output)
        self.assertFalse(state["saver"])
        self.assertNotIn("cmd netpolicy set restrict-background true", self.commands)


if __name__ == "__main__":
    unittest.main()
