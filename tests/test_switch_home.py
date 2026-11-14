"""switch-home.sh and launcher/install.sh --projectivy against a pretend Fire TV: HOME
goes to one launcher at a time, the choice is recorded, and the way back is complete.

Run: python3 -m unittest discover -s tests -v
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUARD = "tv.dumbtv.home/tv.dumbtv.home.Guard"
PROJECTIVY = "com.spocky.projengmenu"
P_GUARD = f"{PROJECTIVY}/{PROJECTIVY}.services.ProjectivyAccessibilityService"
P_HOME = f"{PROJECTIVY}/.ui.home.MainActivity"
BOUND = ("User state[\n  attributes:{id=0, touchExplorationEnabled=false}\n"
         "  Bound services:{Service[label=Projectivy Launcher, feedbackType[FEEDBACK_GENERIC]]}\n")


class SwitchHomeTest(unittest.TestCase):
    def switch(self, *args, settings=None, projectivy=True, sdk=30, conf="LAUNCHER=1\nHOME_APP=dumbtv\n",
               idle=None):
        packages = {"tv.dumbtv.home": {"system": False, "enabled": True},
                    "com.amazon.tv.launcher": {"system": True, "enabled": True}}
        if projectivy:
            packages[PROJECTIVY] = {"system": False, "enabled": True}
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            state = tmp / "state.json"
            state.write_text(json.dumps({
                "packages": packages, "sdk": sdk, "settings": settings or {},
                "homes": {PROJECTIVY: P_HOME}, "a11y_dump": BOUND, "idle": idle or []}))
            log = tmp / "commands.log"
            log.touch()
            conf_path = tmp / "dumbtv.conf"
            if conf is not None:
                conf_path.write_text(conf)
            env = dict(os.environ, ADB=str(ROOT / "tests" / "fake_tv.py"), ADB_SERIAL="test-tv",
                       FAKE_TV_STATE=str(state), FAKE_TV_LOG=str(log), CONF=str(conf_path),
                       REPORT=str(tmp / "report"))
            result = subprocess.run(["bash", str(ROOT / "scripts" / "switch-home.sh"), *args],
                                    env=env, capture_output=True, text=True, timeout=120)
            return (result, log.read_text().splitlines(), json.loads(state.read_text()),
                    conf_path.read_text() if conf_path.exists() else None)

    def test_projectivy_takes_home_and_the_guard_goes(self):
        result, commands, state, conf = self.switch(
            "projectivy", "-y", settings={
                "secure/enabled_accessibility_services": f"example.reader/.Service:{GUARD}",
                "global/alarm_manager_constants": "min_futurity=0"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        settings = state["settings"]
        self.assertEqual(settings["secure/enabled_accessibility_services"], f"example.reader/.Service:{P_GUARD}")
        self.assertEqual(settings["global/dumbtv_home"], "projectivy")
        # Only dumbtv home's Guard needs the alarm setting; it goes with the Guard.
        self.assertNotIn("global/alarm_manager_constants", settings)
        self.assertIn(PROJECTIVY, state["idle"])
        self.assertEqual(settings["global/dumbtv_projectivy_idle"], "1")
        self.assertIn(f"am start -W -n {P_HOME}", commands)
        self.assertIn("HOME_APP=projectivy", conf)
        self.assertIn("LAUNCHER=1", conf)
        self.assertEqual(state.get("bad", []), [])

    def test_back_to_dumbtv_conf_lines_are_replaced_not_added(self):
        _, _, _, conf = self.switch("projectivy", "-y", conf="PRIME=1\nLAUNCHER=1\nHOME_APP=dumbtv\n")
        self.assertEqual(conf.count("HOME_APP="), 1)
        self.assertEqual(conf.count("LAUNCHER="), 1)
        self.assertIn("PRIME=1", conf)

    def test_amazon_switches_off_both_catchers_and_only_our_doze_exemption(self):
        result, commands, state, conf = self.switch(
            "amazon", "-y", idle=[PROJECTIVY], settings={
                "secure/enabled_accessibility_services": P_GUARD,
                "global/dumbtv_home": "projectivy",
                "global/dumbtv_projectivy_idle": "1"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        settings = state["settings"]
        self.assertNotIn(P_GUARD, settings.get("secure/enabled_accessibility_services", ""))
        self.assertNotIn("global/dumbtv_home", settings)
        self.assertNotIn("global/dumbtv_projectivy_idle", settings)
        self.assertNotIn(PROJECTIVY, state["idle"])
        self.assertIn("LAUNCHER=0", conf)

    def test_an_exemption_the_owner_made_stays(self):
        result, _, state, _ = self.switch(
            "projectivy", "-y", idle=[PROJECTIVY],
            settings={"secure/enabled_accessibility_services": GUARD})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("global/dumbtv_projectivy_idle", state["settings"])
        result, _, state, _ = self.switch(
            "amazon", "-y", idle=[PROJECTIVY], settings=state["settings"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(PROJECTIVY, state["idle"])

    def test_missing_projectivy_opens_its_appstore_page_and_changes_nothing(self):
        result, commands, state, conf = self.switch(
            "projectivy", "-y", projectivy=False,
            settings={"secure/enabled_accessibility_services": GUARD})
        self.assertEqual(result.returncode, 1)
        self.assertIn("Appstore", result.stderr)
        self.assertTrue(any("amzn://apps/android?p=com.spocky.projengmenu" in c for c in commands), commands)
        self.assertEqual(state["settings"]["secure/enabled_accessibility_services"], GUARD)
        self.assertIn("HOME_APP=dumbtv", conf)
        # Never downloaded: no install of any APK.
        self.assertFalse(any(c.startswith("pm install") for c in commands))

    def test_dry_run_changes_nothing(self):
        result, commands, state, conf = self.switch(
            "projectivy", "--dry-run", settings={"secure/enabled_accessibility_services": GUARD})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[dry-run]", result.stderr)
        self.assertEqual(state["settings"], {"secure/enabled_accessibility_services": GUARD})
        self.assertFalse(any(c.startswith(("settings put", "settings delete")) for c in commands))
        self.assertIn("HOME_APP=dumbtv", conf)

    def test_status_names_two_catchers_as_a_fault(self):
        result, commands, _, _ = self.switch(
            "status", settings={"secure/enabled_accessibility_services": f"{GUARD}:{P_GUARD}"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("HOME opens          both", result.stderr)
        self.assertFalse(any(c.startswith(("settings put", "settings delete")) for c in commands))

    def test_fire_os_6_cannot_hand_home_to_projectivy(self):
        result, _, state, _ = self.switch("projectivy", "-y", sdk=25, settings={})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Fire OS 6", result.stderr)
        self.assertNotIn("global/dumbtv_home", state["settings"])

    def test_restore_hands_home_back_from_projectivy(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            state = tmp / "state.json"
            state.write_text(json.dumps({
                "packages": {PROJECTIVY: {"system": False, "enabled": True}},
                "idle": [PROJECTIVY],
                "settings": {"secure/enabled_accessibility_services": P_GUARD,
                             "secure/accessibility_enabled": "1",
                             "global/dumbtv_home": "projectivy",
                             "global/dumbtv_projectivy_idle": "1"}}))
            log = tmp / "commands.log"
            log.touch()
            (tmp / "dumbtv.conf").write_text("HOME_APP=projectivy\n")
            env = dict(os.environ, ADB=str(ROOT / "tests" / "fake_tv.py"), ADB_SERIAL="test-tv:5555",
                       FAKE_TV_STATE=str(state), FAKE_TV_LOG=str(log), CONF=str(tmp / "dumbtv.conf"),
                       REPORT=str(tmp / "report"), BOOT_SECONDS="0", PM_WRITE_SECONDS="0")
            result = subprocess.run(["bash", str(ROOT / "scripts" / "restore.sh"), "-y"],
                                    env=env, capture_output=True, text=True, timeout=120)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            after = json.loads(state.read_text())
            self.assertNotIn(P_GUARD, after["settings"].get("secure/enabled_accessibility_services", ""))
            self.assertNotIn("global/dumbtv_home", after["settings"])
            self.assertEqual(after["idle"], [])


class ConfigureHomeTest(unittest.TestCase):
    def configure(self, *flags):
        with tempfile.TemporaryDirectory() as tmp:
            conf = Path(tmp) / "dumbtv.conf"
            result = subprocess.run(["bash", str(ROOT / "scripts" / "configure.sh"), "-y", *flags],
                                    env=dict(os.environ, CONF=str(conf)),
                                    capture_output=True, text=True, timeout=30)
            return result, conf.read_text() if conf.exists() else None

    def test_dumbtv_home_is_the_default(self):
        result, conf = self.configure()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("HOME_APP=dumbtv", conf)

    def test_projectivy_can_be_chosen(self):
        result, conf = self.configure("--home", "projectivy")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("HOME_APP=projectivy", conf)

    def test_an_unknown_home_is_refused(self):
        result, conf = self.configure("--home", "nova")
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(conf)


if __name__ == "__main__":
    unittest.main()
