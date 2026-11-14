# Projectivy Launcher with dumbtv

dumbtv installs its own home screen, [dumbtv home](../launcher/README.md). Some people
prefer [Projectivy Launcher](https://projectivylauncher.com/) by Spocky: more themes,
rows you arrange yourself, a "Now Playing" shelf. dumbtv can keep both installed and
let HOME open either one, or Amazon's own home screen.

## Choosing

```sh
./scripts/configure.sh --home projectivy   # recorded in dumbtv.conf; launcher.sh follows it
./scripts/switch-home.sh                   # shows what HOME opens now, then asks
./scripts/switch-home.sh projectivy        # or name it: dumbtv, projectivy, amazon
./scripts/switch-home.sh status            # read-only
./scripts/switch-home.sh dumbtv --dry-run  # what it would do
```

On Windows: `windows\dumbtv switch-home projectivy` ([the wrapper](../windows/)).

What each choice does:

| Choice | HOME catcher enabled | Also |
|---|---|---|
| `dumbtv` | dumbtv home's Guard (`tv.dumbtv.home/.Guard`) | `min_futurity=0` so HOME answers at once; installs or updates dumbtv home from this repo's checksum-verified release |
| `projectivy` | Projectivy's own service (`com.spocky.projengmenu/...ProjectivyAccessibilityService`) | dumbtv home's Guard and its alarm setting are removed; Projectivy is exempted from doze if it was not already |
| `amazon` | none | both launchers stay installed and unused |

Fire OS 8 ignores the "default home" setting and will not let anyone disable
`com.amazon.tv.launcher`, so neither launcher can simply become the default. Each one
catches the HOME key with an accessibility service and puts itself in front. Two
catchers would fight over every press, so `launcher/install.sh` only ever leaves one
of them in `enabled_accessibility_services`: enabling one removes the other.
`verify.sh` fails when both are on, and `switch-home.sh status` and `health.sh` say so.

The choice is kept in two places: `dumbtv.conf` (`LAUNCHER`, `HOME_APP`), which the
scripts read, and the TV itself (`settings global dumbtv_home`), so a second computer
sees the same state. `./scripts/restore.sh` switches off both catchers, removes the doze
exemption only if dumbtv added it, and clears `dumbtv_home`: HOME is Amazon's again
and both apps stay installed.

Fire OS 6 refuses third-party accessibility services, so only dumbtv home's Keeper can
hold HOME there; `projectivy` is refused on those TVs.

## Installing Projectivy

dumbtv never downloads, mirrors or rehosts Projectivy's APK. It is closed source and
comes from its developer through:

- the [Amazon Appstore](https://www.amazon.com/dp/B0FVKHYHFL) (`amzn://apps/android?p=com.spocky.projengmenu`),
  which keeps it updated and carries the premium unlock;
- [Google Play](https://play.google.com/store/apps/details?id=com.spocky.projengmenu), for Android TV;
- the developer's [GitHub releases](https://github.com/spocky/miproja1/releases).

When `HOME_APP=projectivy` and Projectivy is missing, `launcher.sh` and
`switch-home.sh projectivy` open its Appstore page on the TV and stop; install it there
with the remote and run the command again. The developer notes that the Appstore build
and the GitHub build are signed differently: switching between them means backing up
Projectivy's settings, uninstalling, and installing the other one.

Already installed? Nothing to do: `switch-home.sh projectivy` uses the copy on the TV.

## Inside Projectivy

From [FireDebloat's Projectivy guide](https://github.com/krishkatyal/FireDebloat/blob/main/docs/PROJECTIVY_GUIDE.md)
by Krish Katyal (MIT, see [CREDITS.md](../CREDITS.md)), adjusted to how dumbtv works:

- **Override current launcher.** Projectivy Settings (the gear) > General > *Override
  current launcher*: on. If HOME still lands on Amazon's home, also try *Alternate
  remote detection*. `switch-home.sh` enables Projectivy's accessibility service for
  you; there is no need to toggle it in Settings > Accessibility.
- **Doze.** A launcher that Android dozes answers HOME a second or two late.
  `switch-home.sh projectivy` runs `dumpsys deviceidle whitelist +com.spocky.projengmenu`
  when the exemption is missing, and restore takes it away again.
- **Now Playing shelf.** Fire OS has no Android TV channels, so Projectivy's resume
  cards come from media sessions and need notification access. Grant it when
  Projectivy asks. dumbtv does not set it: the one-line
  `settings put secure enabled_notification_listeners ...` found in some guides
  replaces the whole list and silently takes notification access from every other
  app.
- **Rows.** One way to keep it tidy: favourites first, then streaming apps, then
  system tools (Settings, a file manager), and hide Amazon's own categories under
  *Edit categories*.

dumbtv home keeps running in the background when Projectivy is the home screen, and
still restarts the DNS filter after Android kills it.

## Proton VPN and other VPN apps

Unrelated to the launcher, but common on the same TVs: personalDNSfilter is a VPN, and
Android runs one VPN at a time. With Proton VPN (or another app in
[`data/vpn-apps.txt`](../data/vpn-apps.txt), or any app holding always-on VPN) on the
TV, `dnsfilter.sh` leaves it alone and skips the filter, and `verify.sh` skips the DNS
checks. Choose `--dnsfilter 0` in `configure.sh` to stop the reminder.
