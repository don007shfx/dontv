"""windows/dumbtv.ps1 hands a script and its flags to bash unchanged, and refuses names
that are not scripts. Skipped where PowerShell (pwsh) is not installed; GitHub's Ubuntu
runners have it.

Run: python3 -m unittest discover -s tests -v
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PWSH = shutil.which("pwsh") or shutil.which("powershell")


@unittest.skipUnless(PWSH, "PowerShell is not installed")
class WindowsWrapperTest(unittest.TestCase):
    def run_ps(self, *args, **env):
        return subprocess.run([PWSH, "-NoProfile", "-File", str(ROOT / "windows" / "dumbtv.ps1"), *args],
                              env=dict(os.environ, DUMBTV_BASH=shutil.which("bash"),
                                       ADB=str(ROOT / "tests" / "fake_tv.py"), **env),
                              capture_output=True, text=True, timeout=120)

    def test_flags_reach_the_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_ps("configure", "-y", "--dry-run", "--home", "projectivy",
                                 CONF=str(Path(tmp) / "dumbtv.conf"))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("HOME_APP=projectivy", result.stdout + result.stderr)
            self.assertFalse((Path(tmp) / "dumbtv.conf").exists())

    def test_helpers_and_unknown_names_are_refused(self):
        for name in ("lib", "nope"):
            with self.subTest(name=name):
                result = self.run_ps(name)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_help_lists_the_scripts(self):
        result = self.run_ps("help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("preflight", "all", "switch-home", "health", "restore", "repair"):
            self.assertIn(name, result.stdout)
        self.assertNotIn("lib,", result.stdout)


class WindowsFilesTest(unittest.TestCase):
    def test_batch_file_calls_the_powershell_wrapper(self):
        text = (ROOT / "windows" / "dumbtv.cmd").read_text()
        self.assertIn('-File "%~dp0dumbtv.ps1" %*', text)

    def test_line_endings_are_crlf_on_checkout(self):
        attrs = (ROOT / ".gitattributes").read_text()
        self.assertIn("*.cmd text eol=crlf", attrs)


if __name__ == "__main__":
    unittest.main()
