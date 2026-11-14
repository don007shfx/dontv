"""docs/PACKAGES.md says what dumbtv does with each package; the lists in data/fireos
are what it really does. A list change that the table does not follow fails here.

Run: python3 -m unittest discover -s tests -v
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "fireos"


def entries(path):
    out = set()
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.add(line.split()[0])
    return out


LISTS = {
    "disabled": entries(DATA / "packages.txt"),
    "ALEXA=0": entries(DATA / "alexa.txt"),
    "if named": entries(DATA / "user-apps.txt"),
    "protected": entries(DATA / "protected.txt"),
    "never": entries(DATA / "never-disable.txt"),
}


def rows():
    text = (ROOT / "docs" / "PACKAGES.md").read_text()
    table = text.split("| Package | What it does | Without it | Verdict | dumbtv |", 1)[1]
    table = table.split("\n## ", 1)[0]
    for line in table.splitlines():
        m = re.match(r"\| `([^`]+)` \|.*\| ([^|]+) \|$", line)
        if m:
            yield m.group(1), m.group(2).strip()


class PackagesDocTest(unittest.TestCase):
    def test_the_dumbtv_column_matches_the_lists(self):
        checked = 0
        for package, column in rows():
            if "*" in package:
                continue
            with self.subTest(package=package):
                where = [name for name, found in LISTS.items() if package in found]
                self.assertEqual(where, [] if column == "—" else [column])
                checked += 1
        self.assertGreater(checked, 50)

    def test_each_package_has_one_row(self):
        names = [p for p, _ in rows()]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
