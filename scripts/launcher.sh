#!/usr/bin/env bash
# Installs dumbtv home (this repo's own launcher, launcher/) and gives it the
# HOME button. Fire OS ignores "default home" and protects Amazon's launcher, so
# the takeover runs through a small accessibility service (Fire OS 7/8) or the
# UsageStats Keeper (Fire OS 6, which refuses third-party accessibility services);
# launcher/README.md has the details. With HOME_APP=projectivy in dumbtv.conf, dumbtv home
# is still installed, and HOME then goes to Projectivy Launcher instead (docs/PROJECTIVY.md);
# ./scripts/switch-home.sh changes between them later.
# Usage: ./scripts/launcher.sh [--dry-run] [-y]
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
parse_flags "$@"
need_device
load_conf

if [[ $LAUNCHER == 0 ]]; then
  note "LAUNCHER=0 in dumbtv.conf — keeping Amazon's home screen. Re-run ./scripts/configure.sh to change that."
  exit 0
fi

PKG=tv.dumbtv.home
WANT=$(home_pkg)

step "plan"
note "install dumbtv home: open source, 116 KB, no internet permission, no ad ID"
note "the prebuilt APK comes from this repo's GitHub release and is checksum-verified"
if [[ $SDK -lt 28 ]]; then
  note "take over HOME: Keeper (UsageStats + moveTaskToFront, no accessibility)"
else
  note "take over HOME: accessibility service + alarm min_futurity=0"
fi
note "Amazon's launcher stays installed: hold HOME for Fire OS's menu, or Options > Open Amazon's home screen"
if [[ $HOME_APP == projectivy ]]; then
  [[ $SDK -ge 28 ]] || die "HOME_APP=projectivy: Fire OS 6 refuses Projectivy's accessibility service; run ./scripts/configure.sh --home dumbtv"
  if present "$PROJECTIVY_PKG"; then
    note "then hand HOME to Projectivy Launcher (HOME_APP=projectivy); dumbtv home's Guard is switched off"
  else
    note "Projectivy Launcher is not installed: its Amazon Appstore page opens on the TV; HOME stays on dumbtv home until it is"
  fi
fi
if [[ $DRY_RUN == 1 ]]; then
  note "[dry-run] ADB=$ADB ADB_SERIAL=$SERIAL launcher/install.sh"
  [[ $HOME_APP == projectivy ]] && note "[dry-run] ADB=$ADB ADB_SERIAL=$SERIAL launcher/install.sh --projectivy"
  exit 0
fi
confirm "Replace the home screen on $SERIAL?" || die "cancelled"

ADB=$ADB ADB_SERIAL=$SERIAL "$ROOT/launcher/install.sh" || die "launcher install failed (see above)"
if [[ $HOME_APP == projectivy ]]; then
  if present "$PROJECTIVY_PKG"; then
    ADB=$ADB ADB_SERIAL=$SERIAL "$ROOT/launcher/install.sh" --projectivy || die "could not hand HOME to Projectivy (see above)"
  else
    dev "am start -a android.intent.action.VIEW -d '$PROJECTIVY_STORE'" >/dev/null
    note "Projectivy Launcher's Appstore page is open on the TV. Install it there, then run"
    note "./scripts/switch-home.sh projectivy. Until then HOME opens dumbtv home."
    WANT=$PKG
  fi
fi

for _ in 1 2 3 4 5 6 7 8 9 10; do
  sleep 1
  home=$(front_activity)
  [[ $home == "$WANT"/* ]] && break
done
if [[ $home == "$WANT"/* ]]; then
  note "home screen is $(app_name "$WANT" | grep . || echo dumbtv home)"
elif [[ -z $home ]]; then
  note "could not read which app is in front; ./scripts/verify.sh checks the takeover"
elif [[ $home == com.amazon.tv.parentalcontrols/* ]]; then
  note "Fire OS is asking for the parental-controls PIN ($home)"
  note "enter it on the TV, then run this script again"
  exit 1
else
  note "home screen is $home"
  note "press HOME once or run this script again; see docs/TROUBLESHOOTING.md if it will not stick"
  exit 1
fi
