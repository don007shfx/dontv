"""debloat.sh against a pretend Fire TV: what it disables, and what it never touches.

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


CLEANUP = entries(DATA / "packages.txt")
ALEXA = entries(DATA / "alexa.txt")
USER_APPS = entries(DATA / "user-apps.txt")
STORE_APPS = ["com.netflix.ninja", "com.amazon.firetv.youtube", "org.videolan.vlc",
              "in.startv.hotstar", "com.zee5.amazon"]


class DebloatTest(unittest.TestCase):
    AMAZON_DREAM = "com.amazon.ftv.screensaver/.app.services.ScreensaverService"

    def run_debloat(self, conf="", *flags, basic_dream=True, extra=None, home_activities=None,
                    props=None, previous=None):
        packages = {p: {"system": True, "enabled": True} for p in CLEANUP + ALEXA + USER_APPS}
        packages.update(extra or {})
        if basic_dream:
            packages["com.android.dreams.basic"] = {"system": True, "enabled": True}
        for p in STORE_APPS:
            packages[p] = {"system": False, "enabled": True}
        packages["com.amazon.tv.launcher"] = {"system": True, "enabled": True}
        packages["com.amazon.device.metrics"] = {"system": True, "enabled": True, "protected": True}
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            state = tmp / "state.json"
            state.write_text(json.dumps({"packages": packages, "settings": {
                "secure/screensaver_components": self.AMAZON_DREAM},
                "home_activities": home_activities or [], "props": props or {}}))
            if previous is not None:
                (tmp / "report").mkdir()
                (tmp / "report" / "debloat.txt").write_text(previous)
            log = tmp / "commands.log"
            log.touch()
            (tmp / "dumbtv.conf").write_text(conf)
            env = dict(os.environ, ADB=str(ROOT / "tests" / "fake_tv.py"), ADB_SERIAL="test-tv",
                       FAKE_TV_STATE=str(state), FAKE_TV_LOG=str(log), CONF=str(tmp / "dumbtv.conf"),
                       REPORT=str(tmp / "report"))
            env.pop("REMOVE_EXTRA", None)
            env.pop("KEEP_APPS", None)
            env.pop("ALEXA", None)
            result = subprocess.run(
                ["bash", str(ROOT / "scripts" / "debloat.sh"), "-y", "--no-reboot", *flags],
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            commands = log.read_text().splitlines()
            self.commands, self.output = commands, result.stdout + result.stderr
            report = tmp / "report" / "debloat.txt"
            self.report = report.read_text().splitlines() if report.exists() else None
        disabled = {c.split()[-1] for c in commands if c.startswith("pm disable-user")}
        uninstalled = {c.split()[-1] for c in commands if c.startswith("pm uninstall")}
        settings = [c for c in commands if c.startswith("settings put")]
        return disabled, uninstalled, settings

    def test_the_log_goes_to_the_report_folder_given(self):
        # A test run must never overwrite the owner's real report/debloat.txt.
        self.run_debloat()
        self.assertIsNotNone(self.report, "debloat.txt was not written to REPORT")
        self.assertTrue(any(line.endswith("\tdisabled") for line in self.report))

    def test_default_touches_no_app(self):
        disabled, uninstalled, _ = self.run_debloat()
        self.assertEqual(uninstalled, set())
        self.assertEqual(disabled, set(CLEANUP))
        self.assertFalse(disabled & set(USER_APPS + STORE_APPS))

    def test_default_keeps_alexa_and_voice(self):
        disabled, _, settings = self.run_debloat()
        self.assertFalse(disabled & set(ALEXA))
        self.assertFalse([s for s in settings if "voice_disabled" in s or "alexa_wake_word" in s])

    def test_alexa_off_only_when_asked(self):
        disabled, _, settings = self.run_debloat("ALEXA=0\n")
        self.assertTrue(set(ALEXA) <= disabled)
        self.assertTrue([s for s in settings if "voice_disabled" in s])

    def test_only_named_apps_are_removed(self):
        conf = 'REMOVE_EXTRA="in.startv.hotstar com.amazon.cloud9"\n'
        disabled, uninstalled, _ = self.run_debloat(conf)
        self.assertEqual(uninstalled, {"in.startv.hotstar"})
        self.assertIn("com.amazon.cloud9", disabled)
        self.assertNotIn("com.zee5.amazon", uninstalled | disabled)
        self.assertNotIn("com.amazon.firetv.youtube", uninstalled | disabled)

    def test_never_disable_wins_over_a_named_app(self):
        disabled, uninstalled, _ = self.run_debloat('REMOVE_EXTRA="com.amazon.tv.launcher"\n')
        self.assertNotIn("com.amazon.tv.launcher", disabled | uninstalled)

    def test_keep_list_wins_over_the_cleanup_list(self):
        disabled, _, _ = self.run_debloat('KEEP_APPS="com.amazon.tv.acr"\n')
        self.assertNotIn("com.amazon.tv.acr", disabled)

    def test_screensaver_left_alone_by_default(self):
        _, _, settings = self.run_debloat()
        self.assertFalse([s for s in settings if "screensaver" in s])

    def test_disabled_screensaver_is_replaced_by_androids_own(self):
        disabled, _, settings = self.run_debloat('REMOVE_EXTRA="com.amazon.ftv.screensaver"\n')
        self.assertIn("com.amazon.ftv.screensaver", disabled)
        self.assertIn("settings put secure screensaver_components com.android.dreams.basic/.Colors",
                      settings)

    def test_no_replacement_screensaver_means_no_change(self):
        _, _, settings = self.run_debloat('REMOVE_EXTRA="com.amazon.ftv.screensaver"\n',
                                          basic_dream=False)
        self.assertFalse([s for s in settings if "screensaver" in s])

    def test_a_needed_package_an_old_list_disabled_is_enabled_again(self):
        # dumbtv disabled com.amazon.firebat (Prime Video) until October 2026 (#175).
        self.run_debloat(extra={"com.amazon.firebat": {"system": True, "enabled": False}})
        self.assertIn("pm enable --user 0 com.amazon.firebat", self.commands)
        self.assertIn("enabled again (an older dumbtv had disabled it)", self.output)
        self.assertIn("com.amazon.firebat\tenabled-again", self.report)

    def test_a_needed_package_the_system_ships_disabled_stays_off(self):
        self.run_debloat(extra={"com.amazon.tv.livetv": {"system": True, "enabled": False,
                                                         "system_disabled": True}})
        self.assertIn("off, left as it is", self.output)
        self.assertFalse(any("livetv\tenabled-again" in line for line in self.report))

    def test_enabled_packages_the_tv_needs_are_not_touched(self):
        self.run_debloat(extra={"com.amazon.firebat": {"system": True, "enabled": True}})
        self.assertFalse(any(c.startswith("pm enable") for c in self.commands), self.commands)
        self.assertIn("none of them is off", self.output)

    def test_boot_guard_skips_a_persistent_package(self):
        victim = CLEANUP[0]
        disabled, _, _ = self.run_debloat(extra={victim: {"system": True, "enabled": True,
                                                          "persistent": True}})
        self.assertNotIn(victim, disabled)
        self.assertIn(f"{victim}\tboot-guard\tpersistent process", self.report)
        self.assertIn("SKIP (boot guard: persistent process)", self.output)

    def test_boot_guard_skips_a_package_that_answers_home(self):
        conf = 'REMOVE_EXTRA="com.example.myhome"\n'
        disabled, uninstalled, _ = self.run_debloat(
            conf, extra={"com.example.myhome": {"system": True, "enabled": True}},
            home_activities=["com.example.myhome", "com.amazon.tv.launcher"])
        self.assertNotIn("com.example.myhome", disabled | uninstalled)
        self.assertIn("boot guard: answers HOME", self.output)

    def test_boot_guard_refuses_remote_voice_and_keyboard_by_name(self):
        named = ["com.example.remotecontrol", "com.example.voice.search", "com.example.inputmethod",
                 "com.example.hdmicec", "com.example.setupwizard"]
        conf = 'REMOVE_EXTRA="' + " ".join(named) + '"\n'
        disabled, uninstalled, _ = self.run_debloat(
            conf, extra={p: {"system": True, "enabled": True} for p in named})
        self.assertEqual((disabled | uninstalled) & set(named), set())

    def test_boot_guard_in_the_dry_run(self):
        victim = CLEANUP[0]
        disabled, _, _ = self.run_debloat("", "--dry-run", extra={
            victim: {"system": True, "enabled": True, "persistent": True}})
        self.assertEqual(disabled, set())
        self.assertIn(f"{victim}  SKIP (boot guard: persistent process)", self.output)

    def test_no_list_entry_trips_the_name_rules(self):
        # The guard is a safety net: every reviewed entry must still get through it.
        names = []
        for platform in ("fireos", "fireos6"):
            for name in ("packages.txt", "alexa.txt", "user-apps.txt"):
                path = ROOT / "data" / platform / name
                if path.exists():
                    names += entries(path)
        script = 'source scripts/lib.sh; for p in "$@"; do boot_needed_name "$p" && echo "$p $BOOT_WHY"; done; true'
        out = subprocess.run(["bash", "-c", script, "x", *names], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(out, "")

    def test_the_report_names_the_tv(self):
        self.run_debloat(props={"ro.serialno": "G4N0TEST"})
        self.assertEqual(self.report[0], "#device\tG4N0TEST")

    def test_a_package_someone_else_switched_off_is_not_ours(self):
        # With this TV's record, a listed package that is already off but was not disabled
        # by the last pass is left alone and logged as already-off.
        victim, mine = CLEANUP[0], CLEANUP[1]
        previous = f"#device\tG4N0TEST\n{mine}\tdisabled\n"
        disabled, _, _ = self.run_debloat(
            extra={victim: {"system": True, "enabled": False},
                   mine: {"system": True, "enabled": False}},
            props={"ro.serialno": "G4N0TEST"}, previous=previous)
        self.assertNotIn(victim, disabled)
        self.assertIn(mine, disabled)
        self.assertIn(f"{victim}\talready-off", self.report)

    def test_without_a_record_already_off_packages_are_disabled_as_before(self):
        victim = CLEANUP[0]
        disabled, _, _ = self.run_debloat(extra={victim: {"system": True, "enabled": False}})
        self.assertIn(victim, disabled)

    def test_another_tvs_record_is_ignored(self):
        victim = CLEANUP[0]
        disabled, _, _ = self.run_debloat(
            extra={victim: {"system": True, "enabled": False}},
            props={"ro.serialno": "LIVINGROOM"}, previous="#device\tBEDROOM\n")
        self.assertIn(victim, disabled)

    def test_dry_run_changes_nothing(self):
        disabled, uninstalled, settings = self.run_debloat("", "--dry-run")
        self.assertEqual((disabled, uninstalled, settings), (set(), set(), []))


if __name__ == "__main__":
    unittest.main()
