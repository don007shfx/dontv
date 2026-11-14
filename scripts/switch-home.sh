#!/usr/bin/env bash
# Chooses which home screen the HOME button opens: dumbtv home, Projectivy Launcher or
# Amazon's own. Both launchers stay installed; only one of them catches HOME at a time,
# because each does it with its own accessibility service and enabling one removes the
# other (launcher/install.sh). The choice is kept in dumbtv.conf (LAUNCHER, HOME_APP)
# and on the TV (settings global dumbtv_home), and restore.sh undoes it.
# Usage: ./scripts/switch-home.sh [dumbtv|projectivy|amazon|status] [--dry-run] [-y]
#   no choice: shows what HOME opens now, then asks which one to use
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

CHOICE=""
for a in "$@"; do
  case $a in
    dumbtv|projectivy|amazon|status) [[ -z $CHOICE ]] || die "one choice at a time"; CHOICE=$a ;;
    --dry-run) DRY_RUN=1 ;;
    -y|--yes) ASSUME_YES=1 ;;
    *) die "unknown argument: $a (dumbtv, projectivy, amazon, status, --dry-run, -y)" ;;
  esac
done
need_device
need_supported_fireos
load_conf

step "home screens on $SERIAL"
now=$(home_catcher)
note "dumbtv home         $(present tv.dumbtv.home && echo installed || echo 'not installed')"
note "Projectivy Launcher $(present "$PROJECTIVY_PKG" && echo installed || echo 'not installed')"
note "HOME opens          $now$([[ $now == both ]] && echo ' (two catchers enabled: pick one to fix it)')"
note "dumbtv.conf         $([[ $LAUNCHER == 0 ]] && echo amazon || echo "$HOME_APP")"
[[ $CHOICE == status ]] && exit 0

if [[ -z $CHOICE ]]; then
  [[ $ASSUME_YES == 1 ]] && die "-y needs a choice: dumbtv, projectivy or amazon"
  printf '\n  1) dumbtv home\n  2) Projectivy Launcher\n  3) Amazon home (stock)\n' >&2
  printf 'Which one should HOME open? [1-3, Enter to leave it] ' >&2
  read -r n
  case $n in
    1) CHOICE=dumbtv ;; 2) CHOICE=projectivy ;; 3) CHOICE=amazon ;;
    "") note "unchanged"; exit 0 ;;
    *) die "pick 1, 2 or 3" ;;
  esac
fi

# Records the choice in dumbtv.conf, so launcher.sh and verify.sh follow it. A missing
# file is left missing: configure.sh writes the full one.
record_choice() {
  local launcher=1 app=$1 tmp
  if [[ $1 == amazon ]]; then launcher=0; app=$HOME_APP; fi
  [[ -f $CONF ]] || { note "no dumbtv.conf yet; run ./scripts/configure.sh to keep the choice for later runs"; return 0; }
  tmp=$(mktemp "${TMPDIR:-/tmp}/dumbtv-conf.XXXXXX") || die "could not create a temp file"
  grep -vE '^(LAUNCHER|HOME_APP)=' "$CONF" > "$tmp"
  printf 'LAUNCHER=%s\nHOME_APP=%s\n' "$launcher" "$app" >> "$tmp"
  cat "$tmp" > "$CONF" && rm -f "$tmp"
  note "dumbtv.conf: LAUNCHER=$launcher HOME_APP=$app"
}

install_sh() { ADB=$ADB ADB_SERIAL=$SERIAL "$ROOT/launcher/install.sh" "$@"; }

step "switch to $CHOICE"
case $CHOICE in
  dumbtv)
    note "install or update dumbtv home (checksum-verified release), enable its Guard, switch off Projectivy's" ;;
  projectivy)
    [[ $SDK -ge 28 ]] || die "Fire OS 6 refuses Projectivy's accessibility service; only dumbtv home can take HOME here"
    if ! present "$PROJECTIVY_PKG"; then
      note "Projectivy Launcher is not installed. Its official Amazon Appstore page opens on the TV;"
      note "install it there (dumbtv never downloads or mirrors its APK), then run this again."
      acmd am start -a android.intent.action.VIEW -d "'$PROJECTIVY_STORE'" >/dev/null
      exit 1
    fi
    note "enable Projectivy's accessibility service, switch off dumbtv home's Guard (dumbtv home stays installed)" ;;
  amazon)
    note "switch off both catchers and the alarm setting; dumbtv home and Projectivy stay installed" ;;
esac
if [[ $DRY_RUN == 1 ]]; then
  case $CHOICE in
    dumbtv) note "[dry-run] launcher/install.sh" ;;
    projectivy) note "[dry-run] launcher/install.sh --projectivy" ;;
    amazon) note "[dry-run] launcher/install.sh --undo" ;;
  esac
  note "[dry-run] record LAUNCHER/HOME_APP in ${CONF#"$ROOT"/}"
  exit 0
fi
confirm "HOME opens $CHOICE on $SERIAL?" || die "cancelled"

case $CHOICE in
  dumbtv) install_sh || die "dumbtv home could not take HOME (see above)" ;;
  projectivy) install_sh --projectivy || die "Projectivy could not take HOME (see above)" ;;
  amazon) install_sh --undo >/dev/null || die "could not hand HOME back to Amazon's launcher" ;;
esac
record_choice "$CHOICE"
note "HOME opens $(home_catcher) now; ./scripts/verify.sh presses HOME to prove it"
