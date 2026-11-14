<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
    <img src="docs/assets/logo-light.svg" alt="dontv" width="300">
  </picture>
</p>

<p align="center"><b>Your TV should do what you paid for.</b><br>
Ads, tracking and clutter out of your Fire TV. Your apps and HDMI inputs stay.</p>

<p align="center">
  <a href="https://don007shfx.github.io/dontv/"><b>don007shfx.github.io/dontv</b></a> ·
  <a href="https://don007shfx.github.io/dontv/start.html">Get started</a> ·
  <a href="https://don007shfx.github.io/dontv/blocked.html">What it blocks</a> ·
  <a href="https://don007shfx.github.io/dontv/devices.html">Devices</a> ·
  <a href="https://don007shfx.github.io/dontv/help.html">Get help</a>
</p>

<p align="center">
  <a href="https://github.com/humblemuzzu/dumbtv/stargazers"><img src="https://img.shields.io/github/stars/humblemuzzu/dumbtv?style=flat&color=4C8DFF" alt="Stars"></a>
  <a href="https://github.com/humblemuzzu/dumbtv/releases/latest"><img src="https://img.shields.io/github/v/release/humblemuzzu/dumbtv?label=dumbtv%20home&color=4C8DFF" alt="Latest launcher release"></a>
  <a href="https://github.com/humblemuzzu/dumbtv/actions/workflows/validate.yml"><img src="https://github.com/humblemuzzu/dumbtv/actions/workflows/validate.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-4C8DFF" alt="MIT licence"></a>
  <a href="#thanks"><img src="https://img.shields.io/github/contributors/humblemuzzu/dumbtv?color=4C8DFF" alt="Contributors"></a>
</p>

<p align="center">
  <img src="docs/assets/hero.png" alt="dontv home on a television: a clock, an Apps row and an Inputs row" width="880">
</p>

<p align="center"><sub>As seen in
<a href="https://techcrunch.com/2026/10/19/people-are-using-ai-to-make-their-smart-tvs-dumb-again/">TechCrunch</a> ·
<a href="https://www.techradar.com/entertainment/streaming/your-tv-should-do-what-you-paid-for-people-are-vibe-coding-apps-to-banish-ads-from-their-smart-tvs-and-android-tv-and-its-catching-on">TechRadar</a> ·
<a href="https://www.tomsguide.com/ai/people-are-using-ai-to-turn-their-smart-tvs-into-dumb-tvs-and-you-might-want-to-do-the-same">Tom's Guide</a> ·
<a href="https://gizmodo.com/people-using-ai-to-make-smart-tvs-dumb-again-is-the-most-2026-thing-ever-2000828213">Gizmodo</a> ·
<a href="https://www.xda-developers.com/people-are-now-vibe-coding-their-smart-tvs-to-strip-them-of-ads-and-unwanted-features/">XDA</a> ·
<a href="https://itsfoss.com/news/debloat-smart-tv/">It's FOSS</a> ·
<a href="docs/PRESS.md">and more than 150 others</a></sub></p>

---

> **About this fork.** This is [humblemuzzu/dumbtv](https://github.com/humblemuzzu/dumbtv)
> with a few opt-in extras adapted from
> [firetv-safe-debloat](https://github.com/roy9611/firetv-safe-debloat),
> [debloatfiretv](https://github.com/jannikloehr/debloatfiretv) and
> [FireDebloat](https://github.com/krishkatyal/FireDebloat): a choice between dontv home
> and Projectivy Launcher, frame-rate matching, a read-only health readout, a per-package
> research table, Windows wrappers, and a DNS filter that steps aside for Proton VPN and
> other VPN apps. See [What this fork adds](#what-this-fork-adds) and [CREDITS.md](CREDITS.md).

## The story

**dontv** is a fork of [dumbtv](https://github.com/humblemuzzu/dumbtv) by
[@humblemuzzu](https://github.com/humblemuzzu). It was built by combining dumbtv with
features from three other Fire TV debloat repositories:
[firetv-safe-debloat](https://github.com/roy9611/firetv-safe-debloat),
[debloatfiretv](https://github.com/jannikloehr/debloatfiretv) and
[FireDebloat](https://github.com/krishkatyal/FireDebloat).

dumbtv started when its author's Fire TV Edition television had become painful to use:
menus lagged, apps took ages to open, the home screen was mostly ads, and only 129 MB
of memory was free. He had a coding agent clean it up over ADB,
[posted what happened](https://x.com/DevMuzzammil/status/2111595814099591535), and then
[shared the scripts](https://x.com/DevMuzzammil/status/2111912547318395338). Owners of
many other TVs and sticks have since run it and sent back what they found.

> **Note:** the links row at the top points to dontv's own site,
> [don007shfx.github.io/dontv](https://don007shfx.github.io/dontv/). The other web links
> in this README (the badges, the press links, the release links and the remaining
> dumbtv.org links) still point to the original dumbtv site and repository.

A huge thank you to [@humblemuzzu](https://github.com/humblemuzzu) for an excellent
repository. Its careful snapshots, full restore, never-disable lists, device catalog and
dumbtv home launcher are the foundation everything here is built on.

### What dontv adds, and where it came from

- **From [firetv-safe-debloat](https://github.com/roy9611/firetv-safe-debloat)** by
  [@roy9611](https://github.com/roy9611):
  - optional frame-rate matching
  - quieter home-screen autoplay settings
  - Windows `.cmd` and PowerShell wrappers so everything runs from a Windows PC

  Thank you, @roy9611!
- **From [debloatfiretv](https://github.com/jannikloehr/debloatfiretv)** by
  [@jannikloehr](https://github.com/jannikloehr):
  - the per-package research table in [docs/PACKAGES.md](docs/PACKAGES.md), showing
    what each package does, what breaks without it, and a verdict
  - the dry-run-first approach

  Thank you, @jannikloehr!
- **From [FireDebloat](https://github.com/krishkatyal/FireDebloat)** by
  [@krishkatyal](https://github.com/krishkatyal):
  - the read-only health check (`scripts/health.sh`), based on its vibecheck
  - the Projectivy Launcher notes behind the launcher switch (`scripts/switch-home.sh`),
    which lets you choose dontv home, Projectivy or the stock Amazon home screen

  Thank you, @krishkatyal!
- **New in dontv:** the DNS filter steps aside when Proton VPN or another VPN app is
  installed, so the two don't fight over Android's single VPN slot.

All four projects are MIT licensed. Their notices are kept in [CREDITS.md](CREDITS.md).
See [What this fork adds](#what-this-fork-adds) for commands and details.

## What it does

Built for the Fire TV Stick 4K Max (2nd gen). From your computer, over ADB, with no
root:

- **Removes the ads and tracking.** Disables Amazon's sponsored rows, ad
  services, screen fingerprinting (ACR), telemetry and experiments, and turns off
  ad tracking and usage reporting.
- **Blocks what cannot be disabled.** A small open-source DNS filter on the TV
  stops Amazon's telemetry and automatic updates from reaching their servers.
  If Proton VPN or another VPN app is on the TV, the filter skips itself, since
  Android runs only one VPN at a time.
- **Replaces the home screen** with [dontv home](launcher/README.md) (your apps,
  your inputs and a clock; open source, no internet access) or with Projectivy
  Launcher. Switch between them, or back to Amazon's, at any time.
- **Optional extras:** frame-rate matching for smooth 24p films, and quieter
  autoplay on Amazon's home screen.
- **Checks itself.** A read-only health check shows memory, storage, which launcher
  has HOME, and any package an update turned back on.
- **Runs from Windows, macOS or Linux.** Windows wrappers run every script.
- **Leaves your apps alone.** Nothing you watch is removed unless you name it.
- **Can all be undone** with one command.

## Quick start

You need a computer with [`adb`](https://developer.android.com/tools/releases/platform-tools)
and about ten minutes. On the TV, turn on ADB: **Settings → My Fire TV → About**,
press OK on the device name 7 times, then **Developer Options → ADB debugging**.
The TV's IP address is under **Settings → My Fire TV → About → Network**.

**With a coding agent** (Claude Code, Codex, Cursor, Gemini and others): clone this
repository, open the agent in it, and say:

> Clean up my Fire TV. Its IP address is _(the address from the Network screen)_.

It reads [AGENTS.md](AGENTS.md), asks you a few questions, and runs the steps
below.

**By hand:**

```sh
git clone https://github.com/don007shfx/dontv.git && cd dontv
adb connect <tv-ip>:5555        # press Allow on the TV
./scripts/preflight.sh          # what the TV is and what would change; changes nothing
./scripts/configure.sh          # a few questions
./scripts/all.sh --dry-run      # every command the pass would send; changes nothing
./scripts/all.sh                # asks before each step, reboots the TV twice
./scripts/verify.sh             # checks the result
./scripts/health.sh             # memory, storage, launcher, VPN; changes nothing
```

**On Windows** (needs [Git for Windows](https://git-scm.com/download/win)), the
wrapper in [windows/](windows/README.md) runs the same scripts without opening Git
Bash:

```bat
windows\dumbtv preflight
windows\dumbtv configure
windows\dumbtv all --dry-run
windows\dumbtv all
windows\dumbtv verify
```

Every script that changes the TV takes `--dry-run`, which prints each command and
changes nothing, and asks before its first change unless given `-y`. `preflight.sh`,
`verify.sh`, `health.sh` and `switch-home.sh status` never change anything.

To change the home screen later: `./scripts/switch-home.sh` (or
`windows\dumbtv switch-home`). The original project's step-by-step guide is at
[dumbtv.org/start](https://dumbtv.org/start).

## What you choose

`configure.sh` asks, and nothing is decided for you:

| Question | Default |
|---|---|
| Do you watch Prime Video? | yes: its servers stay reachable |
| Keep Alexa and the voice button? | yes |
| Replace Amazon's home screen? | yes |
| Open Projectivy Launcher instead of dontv home? Both stay installed. | no: dontv home |
| Run the DNS filter on the TV? | yes; skipped automatically when Proton VPN or another VPN app is on the TV |
| Replace the YouTube app with SmartTube (no ads, no Shorts)? | no |
| Match the TV's output to each video's frame rate? | no |
| Also turn off the generic autoplay settings on Amazon's home? | no |
| Any apps you want removed? | none |

Your answers are saved in `dumbtv.conf`; run `configure.sh` again to change them.
Each one also has a flag, for example `./scripts/configure.sh --home projectivy
--dnsfilter 0 --framerate 1`. `./scripts/switch-home.sh dumbtv|projectivy|amazon`
changes only the home screen.

## What changes

| | |
|---|---|
| **Amazon packages** | About 50 disabled: ads, sponsored content, ACR, telemetry, crash and usage uploads, experiments, update nags. Disabled, never deleted. |
| **Protected packages** | The few Amazon will not let anyone disable lose background running; the DNS filter blocks what they upload. |
| **Settings** | Ad tracking limited, interest-based ads off, usage reporting off, featured-row trailers off. |
| **Optional settings** | Frame-rate matching and the generic autoplay settings, only if you chose them. The TV's previous values are saved on the TV and put back by restore. |
| **DNS** | [personalDNSfilter](https://github.com/IngoZenz/personaldnsfilter) runs on the TV and blocks about 400 Amazon telemetry, ad and update hosts. YouTube, the Appstore and your other apps are not blocked. Not installed when another VPN app is on the TV. |
| **Home screen** | dontv home or Projectivy instead of Amazon's: no promo tiles, no sponsored rows. Only one of them catches the HOME button at a time. |
| **Your apps** | Untouched. |

[How it works](docs/HOW-IT-WORKS.md) explains each part and why it is needed.
[docs/PACKAGES.md](docs/PACKAGES.md) lists each package, what it does, what breaks
without it and what dontv does with it.

## dontv home

| Rows | Grid | Options |
|---|---|---|
| ![Rows layout](docs/assets/screens/home.png) | ![Grid layout](docs/assets/screens/grid.png) | ![Options](docs/assets/screens/options.png) |

A home screen that shows your apps and your HDMI inputs, and nothing else. Accent
colours, tile sizes, rows or a grid, wallpapers, adaptive backgrounds, renaming and
hiding, and the icons of an icon pack you install, all from the remote. HOME lands on
it in a fraction of a second.

It is dumbtv's launcher, unchanged: plain Java with no libraries and no internet
permission, so it cannot send anything anywhere. On Fire OS 7 and 8 its only
permission is run at startup, used to restart the DNS filter when Android kills it.
The app keeps its original package name (`tv.dumbtv.home`), and `install.sh`
downloads the checksum-verified release from the original dumbtv repository. It
works on its own, without the rest of dontv:

```sh
adb connect <tv-ip>:5555
./launcher/install.sh
```

Prefer Projectivy Launcher? `./scripts/switch-home.sh projectivy` hands HOME to it
and keeps dontv home installed; `./scripts/switch-home.sh dumbtv` switches back.
[docs/PROJECTIVY.md](docs/PROJECTIVY.md) explains how. [launcher/README.md](launcher/README.md)
covers the settings, wallpapers, icon packs and how it takes over the HOME button.

## Tested on

| Device | Fire OS | Notes |
|---|---|---|
| [Fire TV Stick 4K Max, 2nd gen (AFTKRT)](catalog/devices/fireos-amazon-aftkrt.yaml) | 8.1 | The device dontv is built for. dumbtv's full pass was tested on it by [@gerardo-galvez-hl](https://github.com/gerardo-galvez-hl), [@derkstample](https://github.com/derkstample), [@aboubakrine](https://github.com/aboubakrine) and [@s-razaq](https://github.com/s-razaq). |

The devices on [dumbtv's tested list](https://github.com/humblemuzzu/dumbtv#tested-on)
will likely work too, since dontv uses the same scripts and package lists, but they
have not been tested with dontv. Their reports are still in
[catalog/devices/](catalog/devices/).

Android TV and Google TV are not covered by the scripts; see
[cleanyourtv](https://github.com/Gathin23/cleanyourtv). Samsung, LG, Roku and other
TVs give owners no way in; [docs/OTHER-TVS.md](docs/OTHER-TVS.md) explains each one.

**Your TV not here?** Run it, then `./scripts/contribute.sh`. It writes the report
for you. [CONTRIBUTING.md](CONTRIBUTING.md) has the details.

## What this fork adds

All of it is opt-in or read-only, has `--dry-run` where it changes anything, and is
undone by `./scripts/restore.sh`.

| | From | What it is |
|---|---|---|
| **Pick the home screen** | FireDebloat's Projectivy guide | `./scripts/switch-home.sh [dumbtv\|projectivy\|amazon\|status]`, or `configure.sh --home projectivy`. dontv home and Projectivy both stay installed; only one of them catches HOME at a time. [docs/PROJECTIVY.md](docs/PROJECTIVY.md) |
| **Frame-rate matching** | firetv-safe-debloat | `configure.sh --framerate 1`: Match Original Frame Rate, so 24p films play without judder. The TV's own value is kept on the TV and put back by restore. |
| **Quiet home** | firetv-safe-debloat | `configure.sh --quiet-home 1`: also writes the generic `auto_play_video` / `auto_play_audio` keys. dontv already turns off the featured-row trailer and disables `com.amazon.sneakpeek` on every pass. |
| **Health readout** | FireDebloat's vibecheck | `./scripts/health.sh`: RAM, memory pressure, storage, disabled packages, which packages an update switched back on since `debloat.sh` ran (from `report/debloat.txt`), settings that drifted, which launcher catches HOME, who holds the VPN. Changes nothing. |
| **Package research** | debloatfiretv | [docs/PACKAGES.md](docs/PACKAGES.md): what each package does, what breaks without it, a tested verdict, and what dontv does with it, kept in step with `data/` by a test. |
| **Windows** | firetv-safe-debloat's `.bat` files | [windows/](windows/README.md): `dumbtv.cmd` and `dumbtv.ps1` run any script through Git Bash. |
| **VPN apps** | — | personalDNSfilter is a VPN and Android runs one at a time. With Proton VPN or another app from [data/vpn-apps.txt](data/vpn-apps.txt) installed, or any app holding always-on VPN, `dnsfilter.sh` warns and skips instead of pushing it aside. |

On a Fire TV Stick 4K Max (AFTKRT, Fire OS 8) that already has Projectivy and Proton
VPN, the matching run is:

```sh
./scripts/configure.sh --home projectivy --dnsfilter 0
./scripts/all.sh --dry-run      # read it, then
./scripts/all.sh
./scripts/verify.sh
```

## Undo

```sh
./scripts/restore.sh
```

It re-enables every package, clears the app and network rules, puts back the
settings the TV had before (from the snapshot `preflight.sh` takes), removes the
filter and gives HOME back to Amazon. An app you asked to have uninstalled comes
back from the Appstore.

## Good to know

- **Nothing is written to `/system`**, the part of the TV whose modification
  bricks it. A factory reset removes everything dontv did.
- **Fire OS updates are blocked** while the DNS filter runs, since an update would
  switch a lot of this back on. [The FAQ](docs/FAQ.md) explains how to update
  anyway.
- **It cannot replace Fire OS.** The boot chain is locked by Amazon.
  [Here is why](docs/WHY-NOT-REPLACE-OS.md).
- **YouTube ads can't be blocked by DNS.** They come from the same servers as the
  videos. [docs/YOUTUBE.md](docs/YOUTUBE.md) explains, and what to use instead.

## Documentation

| | |
|---|---|
| [dontv website](https://don007shfx.github.io/dontv/) | getting started, what it blocks, devices, help; source in [site/](site/) |
| [dumbtv.org](https://dumbtv.org) | the original dumbtv website: guides, every package, every device |
| [How it works](docs/HOW-IT-WORKS.md) | each part and why it is needed |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | symptoms and fixes |
| [FAQ](docs/FAQ.md) | updates, Prime Video, factory reset, is this legal |
| [Other TVs](docs/OTHER-TVS.md) | Android TV, Samsung, LG, Roku and the rest |
| [YouTube](docs/YOUTUBE.md) | why its ads cannot be blocked, and SmartTube |
| [Why not replace the OS](docs/WHY-NOT-REPLACE-OS.md) | the locked boot chain |
| [dontv home](launcher/README.md) | the launcher |
| [Device catalog](catalog/README.md) | per-model notes |
| [Packages](docs/PACKAGES.md) | each package, what breaks without it, and what dontv does |
| [Projectivy](docs/PROJECTIVY.md) | Projectivy Launcher next to dontv home |
| [Windows](windows/README.md) | running the scripts from Windows |
| [Credits](CREDITS.md) | the projects this fork borrows from, and their licences |
| [AGENTS.md](AGENTS.md) | instructions for coding agents |
| [Press](docs/PRESS.md) | coverage |

## Thanks

To everyone who tested a TV, wrote code, or reported a problem for dumbtv. It works
on all the devices on [dumbtv's tested list](https://github.com/humblemuzzu/dumbtv#tested-on)
because of you, and dontv is built on that work.

<a href="https://github.com/humblemuzzu/dumbtv/graphs/contributors"><img src="https://contrib.rocks/image?repo=humblemuzzu/dumbtv" alt="Contributors"></a>

**Code, fixes and device reports:**
[@fabricio00101](https://github.com/fabricio00101),
[@MrVoicer](https://github.com/MrVoicer),
[@Jovci](https://github.com/Jovci),
[@niz-coder](https://github.com/niz-coder),
[@centsandcode](https://github.com/centsandcode),
[@maam00](https://github.com/maam00),
[@alfibi](https://github.com/alfibi),
[@theChef613](https://github.com/theChef613),
[@rachit-jain](https://github.com/rachit-jain),
[@daviavmello](https://github.com/daviavmello),
[@yuriwc](https://github.com/yuriwc),
[@lsukev](https://github.com/lsukev),
[@dchuk](https://github.com/dchuk),
[@gerardo-galvez-hl](https://github.com/gerardo-galvez-hl),
[@koconnorgit](https://github.com/koconnorgit),
[@pfTheTrial](https://github.com/pfTheTrial),
[@frogu](https://github.com/frogu),
[@podulator](https://github.com/podulator),
[@tkightly](https://github.com/tkightly),
[@OSikorsky](https://github.com/OSikorsky),
[@nolanvargas](https://github.com/nolanvargas),
[@harupong](https://github.com/harupong),
[@gtalusan](https://github.com/gtalusan),
[@B3NR1S](https://github.com/B3NR1S),
[@bglaszcz](https://github.com/bglaszcz),
[@murilaiooo](https://github.com/murilaiooo),
[@dnpkuk](https://github.com/dnpkuk),
[@timcunningham-sv](https://github.com/timcunningham-sv),
[@iotemylabs](https://github.com/iotemylabs),
[@aswinaasokan18-spec](https://github.com/aswinaasokan18-spec),
[@edrmundy](https://github.com/edrmundy),
[@MarioMartReq](https://github.com/MarioMartReq),
[@ravishan16](https://github.com/ravishan16),
[@jonathanrzarzuela-cloud](https://github.com/jonathanrzarzuela-cloud),
[@Loadedrakeman](https://github.com/Loadedrakeman),
[@ryanlucht](https://github.com/ryanlucht),
[@tharun634](https://github.com/tharun634),
[@NimorM](https://github.com/NimorM),
[@RabeJonas](https://github.com/RabeJonas),
[@Prathamesh913](https://github.com/Prathamesh913),
[@zaco-tm](https://github.com/zaco-tm),
[@NeutronZero](https://github.com/NeutronZero),
[@adi-c](https://github.com/adi-c),
[@derkstample](https://github.com/derkstample),
[@KasperHonore](https://github.com/KasperHonore),
[@damsma](https://github.com/damsma),
[@arielvieira](https://github.com/arielvieira),
[@stedrow](https://github.com/stedrow),
[@zekesax](https://github.com/zekesax),
[@1xretr0](https://github.com/1xretr0),
[@aboubakrine](https://github.com/aboubakrine),
[@acornelissen](https://github.com/acornelissen),
[@alexanderkoh](https://github.com/alexanderkoh),
[@Anny0nn](https://github.com/Anny0nn),
[@bring-nirachornkul](https://github.com/bring-nirachornkul),
[@Chartmann96](https://github.com/Chartmann96),
[@dave137-beep](https://github.com/dave137-beep),
[@dcowern](https://github.com/dcowern),
[@dleslie](https://github.com/dleslie),
[@Elv1sh](https://github.com/Elv1sh),
[@gmckeever](https://github.com/gmckeever),
[@JBolanle](https://github.com/JBolanle),
[@Jeff909Dev](https://github.com/Jeff909Dev),
[@jgcoronado](https://github.com/jgcoronado),
[@jlaska](https://github.com/jlaska),
[@jmcerrejon](https://github.com/jmcerrejon),
[@leonardopieralli](https://github.com/leonardopieralli),
[@lisanet](https://github.com/lisanet),
[@lunar-me](https://github.com/lunar-me),
[@Majunko](https://github.com/Majunko),
[@mrbell321](https://github.com/mrbell321),
[@Muffy0906](https://github.com/Muffy0906),
[@mzmonkey](https://github.com/mzmonkey),
[@Namiato](https://github.com/Namiato),
[@nickzocchi](https://github.com/nickzocchi),
[@oddeyed](https://github.com/oddeyed),
[@PazkaL](https://github.com/PazkaL),
[@PicaPicaDev](https://github.com/PicaPicaDev),
[@PirateKng](https://github.com/PirateKng),
[@priyank-saarthios-ai](https://github.com/priyank-saarthios-ai),
[@rawIce](https://github.com/rawIce),
[@rotenaple](https://github.com/rotenaple),
[@Rouchekoff](https://github.com/Rouchekoff),
[@s-razaq](https://github.com/s-razaq),
[@sakalliAI](https://github.com/sakalliAI),
[@SandheepSridar](https://github.com/SandheepSridar),
[@sant1ago](https://github.com/sant1ago),
[@scaongithub](https://github.com/scaongithub),
[@ScottDavidCA](https://github.com/ScottDavidCA),
[@Sj2594](https://github.com/Sj2594),
[@sockmonkey0223](https://github.com/sockmonkey0223),
[@softwaregames1](https://github.com/softwaregames1),
[@sonofamitch86](https://github.com/sonofamitch86),
[@TheiMacNoob](https://github.com/TheiMacNoob),
[@tvenenga](https://github.com/tvenenga),
[@twwebb3](https://github.com/twwebb3),
[@UlisesSnz](https://github.com/UlisesSnz),
[@vibe-code-viking](https://github.com/vibe-code-viking),
[@w3dd1e](https://github.com/w3dd1e),
[@Zarafos](https://github.com/Zarafos)

**Bug reports:**
[@gleesonb](https://github.com/gleesonb),
[@dennus280-ship-it](https://github.com/dennus280-ship-it),
[@FyllyMan](https://github.com/FyllyMan),
[@nairyash](https://github.com/nairyash),
[@PWannop](https://github.com/PWannop),
[@jt-at-home](https://github.com/jt-at-home),
[@thearchivist9778-ai](https://github.com/thearchivist9778-ai),
[@GrackleCrow](https://github.com/GrackleCrow),
[@MisterKOak](https://github.com/MisterKOak),
[@XaeriS](https://github.com/XaeriS),
[@rcarralero](https://github.com/rcarralero),
[@zniehna](https://github.com/zniehna),
[@folliejester](https://github.com/folliejester),
[@alrubearb-sys](https://github.com/alrubearb-sys),
[@rixialmenar](https://github.com/rixialmenar),
[@Dlay2017](https://github.com/Dlay2017),
[@githububub](https://github.com/githububub)

This fork also thanks [roy9611](https://github.com/roy9611)
([firetv-safe-debloat](https://github.com/roy9611/firetv-safe-debloat)),
[Jannik Löhr](https://github.com/jannikloehr)
([debloatfiretv](https://github.com/jannikloehr/debloatfiretv)) and
[Krish Katyal](https://github.com/krishkatyal)
([FireDebloat](https://github.com/krishkatyal/FireDebloat)), whose MIT-licensed work is
adapted here; [CREDITS.md](CREDITS.md) lists what came from each.

And to the projects dumbtv and dontv build on:
[personalDNSfilter](https://github.com/IngoZenz/personaldnsfilter) by Ingo Zenz,
[HaGeZi's DNS blocklists](https://github.com/hagezi/dns-blocklists),
[SmartTube](https://github.com/yuliskov/SmartTube) by Yuriy Liskov, and
[cleanyourtv](https://github.com/Gathin23/cleanyourtv) by
[@Gathin23](https://github.com/Gathin23) for Android TV and Google TV.

## Legal

dontv changes settings on a device you own, through the developer tools the
manufacturer ships. It does not bypass DRM, unlock anything or touch anyone's
account. Fire TV, Fire OS, Alexa and Prime Video are trademarks of Amazon; dontv is
not affiliated with or endorsed by Amazon. dontv is an independent fork and is not
maintained or endorsed by dumbtv's authors. Use it at your own risk.

## Licence

Scripts, docs and the launcher are [MIT](LICENSE). The device catalog is
[CC BY-SA 4.0](catalog/LICENSE). Parts adapted from firetv-safe-debloat, debloatfiretv
and FireDebloat keep their MIT notices in [CREDITS.md](CREDITS.md).

dontv is a fork of [dumbtv](https://github.com/humblemuzzu/dumbtv). The original
copyright notice in [LICENSE](LICENSE) (Copyright (c) 2026 dumbtv contributors) stays
in place, and dontv's changes by [@don007shfx](https://github.com/don007shfx) are
released under the same MIT licence.

dontv bundles none of these, but downloads them when you ask for them:
personalDNSfilter (GPL-2.0) from F-Droid, HaGeZi's Amazon tracker list (GPL-3.0),
and SmartTube (MIT) from its own releases. Projectivy Launcher is never downloaded:
when it is chosen and missing, its Amazon Appstore page opens on the TV.
