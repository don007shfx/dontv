"""The website in site/: builds, covers every list entry, links resolve, no trackers."""
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site"))
import build  # noqa: E402

PAGES = ["index.html", "start.html", "blocked.html", "devices.html", "help.html", "credits.html", "404.html"]
VOID = {"meta", "link", "img", "br", "hr", "source", "input", "base", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors, self.refs, self.imgs, self.ids, self.h1 = [], [], [], [], set(), 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "img":
            self.imgs.append(a)
        for key in ("href", "src", "srcset"):
            if key in a:
                self.refs.append((tag, a[key]))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"</{tag}> closes {self.stack[-1:] or 'nothing'}")
            return
        self.stack.pop()


class SiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = build.build(Path(cls.tmp.name) / "_site")
        cls.pages = {}
        for name in PAGES:
            p = Page()
            p.feed((cls.out / name).read_text())
            cls.pages[name] = p

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_page_is_well_formed_and_accessible(self):
        for name, p in self.pages.items():
            with self.subTest(page=name):
                self.assertEqual(p.errors, [])
                self.assertEqual(p.stack, [])
                self.assertEqual(p.lang, "en")
                self.assertEqual(p.h1, 1)
                self.assertIn("main", p.ids)
                for img in p.imgs:
                    self.assertTrue(img.get("alt"), img)

    def test_local_links_and_assets_resolve(self):
        for name, p in self.pages.items():
            for tag, ref in p.refs:
                if re.match(r"(https?:|mailto:|#)", ref) or (tag == "base" and ref == "/dontv/"):
                    continue
                path = ref.split("#")[0].split("?")[0] or name
                with self.subTest(page=name, ref=ref):
                    self.assertTrue((self.out / path).is_file())

    def test_no_external_scripts_styles_or_trackers(self):
        for name in PAGES:
            text = (self.out / name).read_text()
            with self.subTest(page=name):
                self.assertNotIn("<script", text)
                self.assertNotIn("<iframe", text)
                self.assertNotRegex(text, r'(src|srcset)="https?:')
                self.assertNotRegex(text, r'<link[^>]+href="https?:')
                self.assertNotRegex(text, r"(?i)google-analytics|googletagmanager|gtag\(|plausible\.io|piqo\.app|cookie-consent")

    def test_blocked_page_lists_every_entry(self):
        text = (self.out / "blocked.html").read_text()
        fo = ROOT / "data" / "fireos"
        for f in ("packages.txt", "protected.txt", "alexa.txt", "user-apps.txt", "never-disable.txt"):
            for _, pkg, _ in build.read_list(fo / f):
                with self.subTest(list=f, package=pkg):
                    self.assertIn(f"<code>{pkg}</code>", text)
        for f in ("settings.txt", "settings.framerate.txt", "settings.quiet-home.txt"):
            for ns, key, _ in build.read_settings(fo / f):
                self.assertIn(f"<code>{ns} {key}</code>", text)

    def test_quick_start_matches_the_readme(self):
        readme = (ROOT / "README.md").read_text()
        start = (self.out / "start.html").read_text().replace("&lt;", "<").replace("&gt;", ">")
        for cmd in re.findall(r"^(\./scripts/\S+(?: --dry-run)?|windows\\dumbtv \S+(?: --dry-run)?)",
                              readme.split("## Quick start")[1].split("\n## ")[0], re.M):
            with self.subTest(cmd=cmd):
                self.assertIn(cmd, start)
        self.assertIn("https://github.com/don007shfx/dontv.git", start)

    def test_build_runs_from_the_command_line(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable, str(ROOT / "site" / "build.py"), d + "/out"], check=True,
                           capture_output=True)
            self.assertTrue((Path(d) / "out" / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
