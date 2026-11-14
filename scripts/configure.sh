#!/usr/bin/env bash
# The interview. Writes dumbtv.conf (git-ignored), which debloat.sh, dnsfilter.sh,
# launcher.sh and youtube.sh read. Every default is the safe one: no app is removed
# unless it is named, and Prime Video and Alexa keep working.
# Usage: ./scripts/configure.sh [--remove "pkg pkg"] [--keep "pkg pkg"] [--prime 0|1]
#          [--alexa 0|1] [--launcher 0|1] [--dnsfilter 0|1] [--youtube 0|1]
#          [--system-dns 0|1] [--dns-upstream "ip ip"] [--home dumbtv|projectivy]
#          [--framerate 0|1] [--quiet-home 0|1] [-y] [--dry-run]
# A flag answers its question without asking; -y takes the default for the rest.
# --dns-upstream is optional. Unset, the filter keeps using the router.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

KEEP_ARG=""; REMOVE_ARG=""; ALEXA_ARG=""; SYSTEM_DNS_ARG=""
PRIME_ARG=""; LAUNCHER_ARG=""; DNSFILTER_ARG=""; YOUTUBE_ARG=""
HOME_ARG=""; FRAMERATE_ARG=""; QUIET_HOME_ARG=""
DNS_UPSTREAM_SET=0; DNS_UPSTREAM_ARG=""
flag01() { case $2 in 0|1) ;; *) die "$1 takes 0 or 1, got '$2'" ;; esac; }
while [[ $# -gt 0 ]]; do
  case $1 in
    --keep)       [[ $# -ge 2 ]] || die "--keep takes package names"; KEEP_ARG=$2; shift 2 ;;
    --remove)     [[ $# -ge 2 ]] || die "--remove takes package names"; REMOVE_ARG=$2; shift 2 ;;
    --prime)      flag01 "$1" "${2:-}"; PRIME_ARG=$2; shift 2 ;;
    --alexa)      flag01 "$1" "${2:-}"; ALEXA_ARG=$2; shift 2 ;;
    --launcher)   flag01 "$1" "${2:-}"; LAUNCHER_ARG=$2; shift 2 ;;
    --dnsfilter)  flag01 "$1" "${2:-}"; DNSFILTER_ARG=$2; shift 2 ;;
    --youtube)    flag01 "$1" "${2:-}"; YOUTUBE_ARG=$2; shift 2 ;;
    --system-dns) flag01 "$1" "${2:-}"; SYSTEM_DNS_ARG=$2; shift 2 ;;
    --home)
      case ${2:-} in dumbtv|projectivy) ;; *) die "--home takes dumbtv or projectivy, got '${2:-}'" ;; esac
      HOME_ARG=$2; shift 2 ;;
    --framerate)  flag01 "$1" "${2:-}"; FRAMERATE_ARG=$2; shift 2 ;;
    --quiet-home) flag01 "$1" "${2:-}"; QUIET_HOME_ARG=$2; shift 2 ;;
    --dns-upstream)
      [[ $# -ge 2 ]] || die '--dns-upstream takes resolver IPs; pass "" to clear them'
      DNS_UPSTREAM_SET=1; DNS_UPSTREAM_ARG=$2; shift 2 ;;
    -y|--yes)     ASSUME_YES=1; shift ;;
    --dry-run)    DRY_RUN=1; shift ;;
    *) die "unknown flag: $1" ;;
  esac
done

KEEP=${KEEP_ARG:-}
EXTRA=${REMOVE_ARG:-}

# Prompt on stderr, answer on stdout: $() must capture only 0 or 1.
yn() {
  local prompt=$1 def=$2 a
  if [[ $ASSUME_YES == 1 ]]; then printf '%s' "$def"; return; fi
  if [[ $def == 1 ]]; then printf '%s [Y/n] ' "$prompt" >&2; else printf '%s [y/N] ' "$prompt" >&2; fi
  read -r a
  [[ -z $a ]] && { printf '%s' "$def"; return; }
  case $a in y|Y|yes|YES) printf 1 ;; *) printf 0 ;; esac
}

answer() {
  if [[ -n $1 ]]; then printf '%s' "$1"; else yn "$2" "$3"; fi
}

step "what dumbtv does either way"
note "Disables Amazon's ads, sponsored rows, screen fingerprinting (ACR), telemetry and"
note "experiments, and turns off ad tracking. Your apps are not touched."

step "a few choices"
if [[ $(answer "$PRIME_ARG" "Do you watch Prime Video? (keeps the servers it needs reachable)" 1) == 1 ]]; then
  PRIME=1; note "prime: kept"
else
  PRIME=0; note "prime: its servers are blocked, so it will not play"
fi
ALEXA=$(answer "$ALEXA_ARG" "Keep Alexa and the remote's voice button? (no = Alexa and the microphone app are switched off)" 1)
LAUNCHER=$(answer "$LAUNCHER_ARG" "Replace Amazon's home screen with dumbtv home or Projectivy Launcher (no ads)?" 1)
# Both launchers are installed when LAUNCHER=1; this only picks which one HOME opens.
# scripts/switch-home.sh changes it later without the rest of the questions.
HOME_APP=dumbtv
if [[ $LAUNCHER == 1 ]]; then
  if [[ -n $HOME_ARG ]]; then HOME_APP=$HOME_ARG
  elif [[ $(yn "HOME opens dumbtv home. Open Projectivy Launcher instead? (both stay installed; switch any time with switch-home.sh)" 0) == 1 ]]; then
    HOME_APP=projectivy
  fi
fi
DNSFILTER=$(answer "$DNSFILTER_ARG" "Run the DNS filter on the TV (blocks Amazon telemetry and stops automatic updates)? It is a VPN: with Proton VPN or another VPN app on the TV it is skipped" 1)
SYSTEM_DNS=$(answer "$SYSTEM_DNS_ARG" "Fire OS 6 only: let system apps bypass the filter so the clock syncs? Amazon's system-user apps go unfiltered too" 0)
# Default no: YouTube is the app people actually watch. scripts/youtube.sh is the
# only thing that touches it, and only when this is 1.
if [[ $(answer "$YOUTUBE_ARG" "Replace the YouTube app with SmartTube (no ads, no Shorts)? Your YouTube account and subscriptions are untouched" 0) == 1 ]]; then
  YOUTUBE=1; note "youtube: replaced with SmartTube"
else
  YOUTUBE=0; note "youtube: left alone"
fi

step "optional tweaks"
FRAMERATE=$(answer "$FRAMERATE_ARG" "Match the TV's output to each video's frame rate (smooth 24p films; the screen blanks a second when it switches)?" 0)
QUIET_HOME=$(answer "$QUIET_HOME_ARG" "Also switch off the generic autoplay keys on Amazon's home (video and sound when a tile is focused)?" 0)

if [[ $ASSUME_YES == 0 && -z $REMOVE_ARG ]]; then
  note "Apps are only removed when you name them here. Names to package ids: data/apps.txt"
  printf 'Apps to remove, space separated package names (Enter for none): ' >&2
  read -r extras
  EXTRA="$EXTRA $extras"
fi
if [[ $ASSUME_YES == 0 && -z $KEEP_ARG ]]; then
  printf 'Anything from the cleanup to keep, space separated package names (Enter for none): ' >&2
  read -r more
  KEEP="$KEEP $more"
fi

# awk, not xargs: xargs gives up on a stray quote and the whole list was dropped unnoticed.
KEEP=$(printf '%s\n' "$KEEP" | awk '{$1=$1; print}')
EXTRA=$(printf '%s\n' "$EXTRA" | awk '{$1=$1; print}')
# dumbtv.conf is sourced by every script, so only package names may go into it: a quote
# would break every script, and $(...) would run as a command each time one starts.
for p in $KEEP $EXTRA; do
  [[ $p =~ ^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+$ ]] ||
    die "'$p' is not a package name (like com.netflix.ninja); data/apps.txt maps app names to packages"
done

# A keep entry that is on no list would protect nothing; it is almost always a typo.
known=$(cat "$DATA"/fireos*/packages.txt "$DATA"/fireos/alexa.txt "$DATA"/fireos*/user-apps.txt 2>/dev/null |
  sed 's/#.*//' | awk 'NF {print $1}')
for k in $KEEP; do
  printf '%s\n' $known $EXTRA | grep -qx -- "$k" ||
    die "keep entry '$k' is on no list: dumbtv never touches it, so leave it out (or fix the typo)"
done
never=$(cat "$DATA"/fireos*/never-disable.txt 2>/dev/null | sed 's/#.*//' | awk 'NF {print $1}')
for r in $EXTRA; do
  printf '%s\n' $never | grep -qx -- "$r" &&
    die "'$r' keeps the TV working (data/fireos*/never-disable.txt), so dumbtv will not remove it"
done

# Not asked: an advanced switch for one filter problem (docs/TROUBLESHOOTING.md). Keep a set value.
FILTER_AUTOSTART=$([[ -f $CONF ]] && sed -n 's/^FILTER_AUTOSTART=//p' "$CONF" | tail -1)
FILTER_AUTOSTART=${FILTER_AUTOSTART:-1}
# Not asked. Resolver IPs for names the local list does not cover. Empty keeps the router.
if [[ $DNS_UPSTREAM_SET == 1 ]]; then
  DNS_UPSTREAM=$DNS_UPSTREAM_ARG
elif [[ -f $CONF ]]; then
  DNS_UPSTREAM=$(sed -n 's/^DNS_UPSTREAM=//p' "$CONF" | tail -1 | tr -d '"')
else
  DNS_UPSTREAM=""
fi
DNS_UPSTREAM=$(printf '%s\n' "$DNS_UPSTREAM" | awk '{$1=$1; print}')
fallback_dns >/dev/null || exit 1

if [[ $DRY_RUN == 1 ]]; then
  step "would write $CONF"
  note "REMOVE_EXTRA=\"$EXTRA\""
  note "KEEP_APPS=\"$KEEP\""
  note "PRIME=$PRIME ALEXA=$ALEXA LAUNCHER=$LAUNCHER DNSFILTER=$DNSFILTER SYSTEM_DNS=$SYSTEM_DNS YOUTUBE=$YOUTUBE"
  note "HOME_APP=$HOME_APP FRAMERATE=$FRAMERATE QUIET_HOME=$QUIET_HOME"
  note "DNS_UPSTREAM=\"${DNS_UPSTREAM:-}\""
  exit 0
fi

mkdir -p "$REPORT"
cat > "$CONF" <<EOF_CONF
# Written by scripts/configure.sh. Git-ignored; it describes this household, not the repo.
REMOVE_EXTRA="$EXTRA"
KEEP_APPS="$KEEP"
PRIME=$PRIME
ALEXA=$ALEXA
LAUNCHER=$LAUNCHER
DNSFILTER=$DNSFILTER
SYSTEM_DNS=$SYSTEM_DNS
YOUTUBE=$YOUTUBE
FILTER_AUTOSTART=$FILTER_AUTOSTART
DNS_UPSTREAM="$DNS_UPSTREAM"
HOME_APP=$HOME_APP
FRAMERATE=$FRAMERATE
QUIET_HOME=$QUIET_HOME
EOF_CONF

# Prove the file before anyone sources it.
# shellcheck disable=SC1090
source "$CONF"
for v in PRIME ALEXA LAUNCHER DNSFILTER SYSTEM_DNS YOUTUBE FILTER_AUTOSTART FRAMERATE QUIET_HOME; do
  case ${!v} in 0|1) ;; *) die "$v must be 0 or 1 in $CONF" ;; esac
done

step "saved"
note "${CONF#$ROOT/}"
note "remove:  ${EXTRA:-nothing}"
note "keep:    ${KEEP:-nothing extra}"
note "prime=$PRIME alexa=$ALEXA launcher=$LAUNCHER dnsfilter=$DNSFILTER system_dns=$SYSTEM_DNS youtube=$YOUTUBE"
note "dns upstream: ${DNS_UPSTREAM:-the router}"
note "home=$([[ $LAUNCHER == 1 ]] && echo "$HOME_APP" || echo amazon) framerate=$FRAMERATE quiet_home=$QUIET_HOME"
note "change any answer later by running this again"
