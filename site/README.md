# dontv website

The site at https://don007shfx.github.io/dontv/. Plain HTML and CSS, no JavaScript,
no web fonts, no analytics.

```sh
python3 site/build.py        # writes _site/
python3 -m http.server -d _site 8000
```

- `pages/*.html` are page bodies; `build.py` wraps them in the shared header and footer.
- `blocked.html` is generated from `data/fireos/` and `docs/PACKAGES.md`, so it always
  matches what the scripts do.
- `.github/workflows/pages.yml` builds and publishes it on every push to `main` that
  touches the site, the data lists or the assets.
- `tests/test_site.py` checks that it builds, links resolve and every listed package
  appears.

`404.html` uses `<base href="/dontv/">`; change it in `build.py` if the site moves.
