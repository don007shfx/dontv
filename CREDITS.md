# Credits and notices

This fork of [dumbtv](https://github.com/humblemuzzu/dumbtv) (MIT, Copyright (c) 2026
dumbtv contributors, see [LICENSE](LICENSE)) adds features adapted from four other MIT
projects. Their copyright notices and licence text are kept below, as the MIT licence
requires. The device catalog in [catalog/](catalog/) stays under CC BY-SA 4.0
([catalog/LICENSE](catalog/LICENSE)).

| Project | What came from it | Where it lives here |
|---|---|---|
| [firetv-safe-debloat](https://github.com/roy9611/firetv-safe-debloat) by roy9611 | Match Original Frame Rate (`match_content_frame_rate`); the `auto_play_video` / `auto_play_audio` keys for home-screen autoplay; the idea of Windows wrappers so a Windows PC can run it | `data/fireos/settings.framerate.txt`, `data/fireos/settings.quiet-home.txt` (opt-in through `configure.sh`, applied by `debloat.sh`, undone by `restore.sh`); `windows/` |
| [debloatfiretv](https://github.com/jannikloehr/debloatfiretv) by Jannik Löhr | The per-package research table: what each package does, what breaks without it, and a verdict tested on a Fire TV 2-Series | `docs/PACKAGES.md` |
| [couch-tv](https://github.com/Seagey/couch-tv) by Seagey | The live "needed to boot?" check (`needed()` in `tv-home/tools/apply.sh`), adapted to Fire OS names; the idea of an undo list holding only what the tool switched off, and of repairing only what an update undid; `com.amazon.kso.blackbird` from its privacy list | `boot_needed` in `scripts/lib.sh` (used by `debloat.sh` and `repair.sh`), `scripts/restore.sh`, `scripts/repair.sh`, `data/fireos/packages.txt` |
| [FireDebloat](https://github.com/krishkatyal/FireDebloat) by Krish Katyal | The `vibecheck.sh` health readout (RAM, storage, disabled packages, launcher state); the Projectivy Launcher guide (override, doze exemption, Now Playing, rows) | `scripts/health.sh`, `docs/PROJECTIVY.md` |

Deliberately not taken: firetv-safe-debloat's background-process limit and cache
trimming; FireDebloat's 104-package list, Private DNS forcing, location kill switch and
notification-listener overwrite; debloatfiretv's lists themselves (dumbtv's lists differ
on a few packages for reasons given in `docs/PACKAGES.md`).

Downloaded on demand, never bundled (unchanged from dumbtv): personalDNSfilter
(GPL-2.0) from F-Droid, HaGeZi's Amazon tracker list (GPL-3.0), SmartTube (MIT) from
its releases. Projectivy Launcher (closed source) is only ever opened in the Amazon
Appstore on the TV.

---

## firetv-safe-debloat

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## debloatfiretv

```
MIT License

Copyright (c) 2026 Jannik Löhr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## FireDebloat

```
MIT License

Copyright (c) 2026 Krish Katyal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## couch-tv

```
MIT License

Copyright (c) 2026 Seagey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
