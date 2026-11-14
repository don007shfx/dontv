#!/usr/bin/env python3
"""Build the dontv website into a folder of static files (default: _site/).

    python3 site/build.py [out-dir]

Plain HTML and CSS, standard library only. The pages in site/pages/ are fragments;
this wraps each one in the shared header and footer. "What it blocks" is generated
from data/fireos/ and docs/PACKAGES.md, so it always matches what the scripts do.
"""
import html
import re
import shutil
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
DATA = ROOT / "data"
REPO = "https://github.com/don007shfx/dontv"

NAV = [
    ("index.html", "Home"),
    ("start.html", "Get started"),
    ("blocked.html", "What it blocks"),
    ("devices.html", "Devices"),
    ("help.html", "Help"),
    ("credits.html", "Credits"),
]

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f4f2ed" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0d10" media="(prefers-color-scheme: dark)">
<meta name="referrer" content="no-referrer">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="dontv home page">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
        <img src="assets/logo-light.svg" alt="dontv" width="92" height="35">
      </picture>
    </a>
    <nav class="nav" aria-label="Main">
      <ul>
{nav}
        <li><a href="{repo}">GitHub</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main" class="wrap">
{body}
</main>
<footer>
  <div class="wrap">
    <p>dontv is a fork of <a href="https://github.com/humblemuzzu/dumbtv">dumbtv</a>.
    MIT licence. Not affiliated with Amazon. No cookies, no tracking.</p>
    <p><a href="{repo}">Source on GitHub</a> · <a href="credits.html">Credits</a></p>
  </div>
</footer>
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=True)


def read_list(path):
    """Entries of a data list: [(section, package, comment)]."""
    out, section = [], ""
    for line in path.read_text().splitlines():
        m = re.match(r"#\s*---\s*(.*?)\s*---\s*$", line)
        if m:
            section = re.sub(r"\s*\(.*\)$", "", m.group(1))
            continue
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pkg, _, comment = line.partition("#")
        out.append((section, pkg.strip(), comment.strip()))
    return out


def read_settings(path):
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            ns, key, value = line.split(None, 2)
            rows.append((ns, key, value))
    return rows


def package_notes():
    """Package -> 'What it does' from docs/PACKAGES.md."""
    notes = {}
    for line in (ROOT / "docs" / "PACKAGES.md").read_text().splitlines():
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*([^|]*)\|", line)
        if m:
            notes.setdefault(m.group(1), m.group(2).strip())  # first table only
    return notes


def pkg_table(rows, notes, caption):
    out = ['<div class="table-wrap"><table>', f"<caption>{esc(caption)}</caption>",
           '<thead><tr><th scope="col">Package</th><th scope="col">What it is</th></tr></thead><tbody>']
    for _, pkg, comment in rows:
        what = comment or notes.get(pkg, "")
        if not what and pkg.startswith("com.amazon.dummy."):
            what = "empty placeholder app"
        what = what[:1].upper() + what[1:] if what else "—"
        out.append(f"<tr><td><code>{esc(pkg)}</code></td><td>{esc(what)}</td></tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def settings_table(rows, caption):
    out = ['<div class="table-wrap"><table>', f"<caption>{esc(caption)}</caption>",
           '<thead><tr><th scope="col">Setting</th><th scope="col">Set to</th></tr></thead><tbody>']
    for ns, key, value in rows:
        out.append(f"<tr><td><code>{esc(ns)} {esc(key)}</code></td><td><code>{esc(value)}</code></td></tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def counts():
    fo = DATA / "fireos"
    return {
        "PACKAGES": len(read_list(fo / "packages.txt")),
        "PROTECTED": len(read_list(fo / "protected.txt")),
        "NEVER": len(read_list(fo / "never-disable.txt")),
        "EXTRA_HOSTS": len(read_list(DATA / "blocklists" / "extra-hosts.txt")),
    }


def blocked_page():
    fo = DATA / "fireos"
    notes = package_notes()
    packages = read_list(fo / "packages.txt")
    c = counts()
    parts = [
        '<p class="eyebrow">What it blocks</p>',
        "<h1>Every switch, in the open.</h1>",
        f'<p class="lead">These lists are generated from the files the scripts read, in '
        f'<a href="{REPO}/tree/main/data/fireos"><code>data/fireos/</code></a>. Packages are '
        "disabled, never deleted, and <code>restore.sh</code> turns every one back on.</p>",
        '<p>For what each package does, what you lose without it and a tested verdict, see '
        f'<a href="{REPO}/blob/main/docs/PACKAGES.md">the package research table</a>.</p>',
        f'<h2 id="disabled">Switched off on every pass <span class="muted">({c["PACKAGES"]})</span></h2>',
        "<p>Ads, tracking, telemetry, experiments, update nags and empty demo apps. "
        "<code>debloat.sh</code> disables these on Fire OS 7 and 8.</p>",
    ]
    sections = []
    for sec, _, _ in packages:
        if sec not in sections:
            sections.append(sec)
    for sec in sections:
        rows = [r for r in packages if r[0] == sec]
        parts.append(f"<h3>{esc(sec[:1].upper() + sec[1:])}</h3>")
        parts.append(pkg_table(rows, notes, f"{sec}: {len(rows)} packages"))

    parts += [
        f'<h2 id="protected">Protected by Amazon <span class="muted">({c["PROTECTED"]})</span></h2>',
        "<p>Fire OS refuses to disable these without root. dontv denies them background running "
        "and background data, and the DNS filter blocks the servers they upload to. The "
        "updater is here, which is why Fire OS updates stop while the filter runs.</p>",
        pkg_table(read_list(fo / "protected.txt"), notes, "Protected packages"),
        '<h2 id="alexa">Alexa, only if you turn it off</h2>',
        "<p>Kept by default so the voice button works. Answer no to Alexa in "
        "<code>configure.sh</code> and these are disabled and Alexa's servers blocked.</p>",
        pkg_table(read_list(fo / "alexa.txt"), notes, "Alexa packages"),
        '<h2 id="apps">Apps, only if you name them</h2>',
        "<p>Things a person might use. dontv never removes them on its own; an app goes only "
        "when you name it in <code>configure.sh</code>.</p>",
        pkg_table(read_list(fo / "user-apps.txt"), notes, "Apps removed only when named"),
        f'<h2 id="never">Never touched <span class="muted">({c["NEVER"]})</span></h2>',
        "<p>The home screen, Settings, inputs, the tuner, remote pairing, Prime Video and what a "
        "factory reset needs. The scripts refuse to disable these, even if you name them.</p>",
        "<details><summary>Show the never-disable list</summary>",
        pkg_table(read_list(fo / "never-disable.txt"), notes, "Never disabled"),
        "</details>",
        '<h2 id="settings">Settings</h2>',
        "<p>Ad tracking limited, interest-based ads and usage reporting off, the featured-row "
        "trailer off, and faster animations. The TV's own values are saved first and put back "
        "by <code>restore.sh</code>.</p>",
        settings_table(read_settings(fo / "settings.txt"), "Applied on every pass"),
        "<p>Optional, only if you choose them in <code>configure.sh</code>:</p>",
        settings_table(read_settings(fo / "settings.framerate.txt"), "Frame-rate matching (--framerate 1)"),
        settings_table(read_settings(fo / "settings.quiet-home.txt"), "Quiet home (--quiet-home 1)"),
        '<h2 id="dns">At the network</h2>',
        '<p>The DNS filter (<a href="https://github.com/IngoZenz/personaldnsfilter">personalDNSfilter</a>) '
        "runs on the TV and blocks Amazon's telemetry, ad and update servers: "
        '<a href="https://github.com/hagezi/dns-blocklists">HaGeZi\'s Amazon tracker list</a> plus '
        f'{c["EXTRA_HOSTS"]} extra hosts read out of Fire OS itself. Prime Video\'s servers stay '
        "reachable unless you say you don't watch it.</p>",
        '<p class="note">If Proton VPN or another VPN app is on the TV, the filter is skipped. '
        "Android runs one VPN at a time, so dontv steps aside instead of fighting your VPN.</p>",
        "<p>Never blocked, and checked by <code>verify.sh</code>:</p><ul>",
    ]
    for _, host, _ in read_list(DATA / "blocklists" / "verify-allowed.txt"):
        parts.append(f"<li><code>{esc(host)}</code></li>")
    parts.append("</ul>")
    return ("What it blocks · dontv",
            "Every package and setting dontv changes on a Fire TV, generated from the repository's lists.",
            "\n".join(parts))


def render(name, title, description, body):
    # 404.html is served for any missing path, so it needs an absolute base.
    base = '<base href="/dontv/">\n' if name == "404.html" else ""
    nav = "\n".join(
        f'        <li><a href="{href}"{" aria-current=\"page\"" if href == name else ""}>{label}</a></li>'
        for href, label in NAV)
    page = LAYOUT.format(base=base, title=esc(title), description=esc(description), nav=nav, body=body, repo=REPO)
    return page.replace('href="#main"', 'href="404.html#main"') if base else page


def fragment(path):
    text = path.read_text()
    meta = dict(re.findall(r"<!--\s*(title|description):\s*(.*?)\s*-->", text))
    body = re.sub(r"<!--\s*(title|description):.*?-->\n?", "", text).strip()
    for key, value in counts().items():
        body = body.replace("{{" + key + "}}", str(value))
    body = body.replace("{{REPO}}", REPO)
    return meta["title"], meta["description"], body


def build(out):
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    (out / "assets" / "screens").mkdir(parents=True)
    shutil.copy(SITE / "style.css", out / "style.css")
    shutil.copy(SITE / "favicon.svg", out / "favicon.svg")
    assets = ROOT / "docs" / "assets"
    for f in ("logo-light.svg", "logo-dark.svg", "hero.png"):
        shutil.copy(assets / f, out / "assets" / f)
    for f in ("home.png", "grid.png", "options.png"):
        shutil.copy(assets / "screens" / f, out / "assets" / "screens" / f)
    for page in sorted((SITE / "pages").glob("*.html")):
        title, description, body = fragment(page)
        (out / page.name).write_text(render(page.name, title, description, body))
    (out / "blocked.html").write_text(render("blocked.html", *blocked_page()))
    (out / ".nojekyll").write_text("")
    return out


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else ROOT / "_site"))
