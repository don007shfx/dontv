#!/usr/bin/env bash
# Read-only health readout: memory, storage, what dumbtv disabled and what a Fire OS
# update has switched back on since, settings that drifted, which home screen catches
# HOME, and who holds the VPN. Changes nothing, so it is safe to run any time, for
# example after the TV updated itself. verify.sh is the pass/fail check; this is the
# wider picture. After FireDebloat's vibecheck.sh (see CREDITS.md).
# Usage: ./scripts/health.sh
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
parse_flags "$@"
need_device
need_supported_fireos
load_conf

attention=0
row() { printf '  %-14s %s\n' "$1" "$2"; }
# Third field of a "Total RAM: 1,234,567K" style line, in MB.
mb() { awk -v k="$1" 'index($0, k) { v = $3; gsub(/[^0-9]/, "", v); printf "%d MB", v / 1024; exit }'; }

step "device"
row model "$(dev1 getprop ro.product.model) ($(fireos_name), $(dev1 getprop ro.build.display.id))"
row uptime "$(dev1 uptime | sed 's/^ *//')"

step "memory"
mem=$(dev 'dumpsys meminfo' | tr -d '\r')
row total "$(printf '%s\n' "$mem" | mb 'Total RAM:')"
row free "$(printf '%s\n' "$mem" | mb 'Free RAM:')"
row used "$(printf '%s\n' "$mem" | mb 'Used RAM:')"
zram=$(printf '%s\n' "$mem" | sed -n 's/^ *ZRAM: *\([0-9,]*\)K physical used.*/\1/p' | tr -d ',' | head -1)
[[ -n $zram ]] && row zram "$((zram / 1024)) MB in use"
level=$(dev 'dumpsys activity' | tr -d '\r' | sed -n 's/.*mLastMemoryLevel=\([A-Za-z_]*\).*/\1/p' | head -1)
row pressure "${level:-not reported by this build}"

step "storage"
df=$(dev 'df -h /data' | tr -d '\r' | awk 'NR > 1 && NF >= 5 { print $2, $3, $4, $5; exit }')
if [[ -n $df ]]; then
  read -r size used avail pct <<<"$df"
  row /data "$used of $size used ($pct), $avail free"
else
  row /data "could not read"
fi

step "packages"
off=$(dev 'pm list packages -d' | tr -d '\r' | sed -n 's/^package://p')
row disabled "$(printf '%s\n' "$off" | grep -c .) packages"
installed=$(dev 'pm list packages' | tr -d '\r' | sed -n 's/^package://p')
# report/debloat.txt is debloat.sh's record of what it disabled on this TV. With a TV per
# room, give each its own REPORT folder, or this compares against the last TV debloated.
back=""
if [[ -f $REPORT/debloat.txt ]]; then
  while IFS=$'\t' read -r p state _; do
    [[ $state == disabled ]] || continue
    grep -qxF "$p" <<<"$installed" || continue
    grep -qxF "$p" <<<"$off" && continue
    back="$back $p"
  done < "$REPORT/debloat.txt"
  row snapshot "${REPORT#"$ROOT"/}/debloat.txt, $(grep -c $'\tdisabled' "$REPORT/debloat.txt") disabled by debloat.sh"
else
  row snapshot "none (debloat.sh has not run from this folder); comparing with the lists instead"
fi
for p in $(cleanup_list); do
  protected_by_policy "$p" && continue
  keep_pkg "$p" && continue
  list_of "$(fos protected.txt)" | grep -qxF "$p" && continue
  grep -qxF "$p" <<<"$installed" || continue
  grep -qxF "$p" <<<"$off" && continue
  case " $back " in *" $p "*) ;; *) back="$back $p" ;; esac
done
if [[ -n $back ]]; then
  row "enabled again" "${back# }"
  row "" "an update switched these back on; ./scripts/repair.sh turns them off again"
  attention=1
else
  row "enabled again" "none"
fi
needed=""
for p in $(list_of "$(fos never-disable.txt)" | awk '{print $1}'); do
  grep -qxF "$p" <<<"$off" || continue
  dev "dumpsys package $p" | grep -q 'User 0:.* enabled=3 ' || continue
  needed="$needed $p"
done
if [[ -n $needed ]]; then row "needed, off" "${needed# }; ./scripts/debloat.sh -y"; attention=1; fi

step "settings"
current=$(dev 'settings list secure; settings list global' | tr -d '\r')
value_of() { printf '%s\n' "$current" | awk -v k="$1" 'index($0, k "=") == 1 { print substr($0, length(k) + 2); exit }'; }
drift=""
while read -r _ key value; do
  [[ $(value_of "$key") == "$value" ]] || drift="$drift $key"
done < <(settings_files | sed 's/ = / /')
if [[ -n $drift ]]; then row privacy "back to Amazon's values:$drift"; attention=1
else row privacy "as set"; fi
while read -r name state file; do
  while read -r _ key value; do
    row "$name" "$key=$(value_of "$key" | grep . || echo unset) (opt-in $state)"
  done < <(list_of "$file")
done < <(optin_tweaks)
# Shown, never changed: a Private DNS host whose certificate is not yet valid at boot
# stopped every lookup on an AFTKRT (catalog/devices/fireos-amazon-aftkrt.yaml).
row "private dns" "$(value_of private_dns_mode | grep . || echo unset)"

step "home"
catcher=$(home_catcher)
row "HOME opens" "$catcher"
row front "$(front_activity | grep . || echo unknown)"
row chosen "$([[ $LAUNCHER == 0 ]] && echo amazon || echo "$HOME_APP") (dumbtv.conf)"
if [[ $catcher == both ]]; then
  row "" "two catchers enabled: ./scripts/switch-home.sh $HOME_APP"; attention=1
elif [[ $LAUNCHER == 1 && $catcher != "$HOME_APP" ]] || [[ $LAUNCHER == 0 && $catcher != amazon ]]; then
  row "" "not the chosen one: ./scripts/switch-home.sh to pick again"; attention=1
fi
if present "$PROJECTIVY_PKG"; then
  idle=$(dev 'dumpsys deviceidle whitelist' | tr -d '\r')
  if grep -q ",$PROJECTIVY_PKG," <<<"$idle"; then row projectivy "installed, exempt from doze"
  else row projectivy "installed, not exempt from doze (HOME can answer late while it is active)"; fi
fi

step "vpn"
always=$(dev1 settings get secure always_on_vpn_app)
row always-on "$([[ -z $always || $always == null ]] && echo none || echo "$always")"
row "dns filter" "$(present dnsfilter.android && echo installed || echo 'not installed')"
vpn_app=$(other_vpn_app)
[[ -n $vpn_app ]] && row "other vpn" "$vpn_app ($(app_name "$vpn_app" | grep . || echo 'VPN app'))"
if [[ -n $vpn_app ]] && present dnsfilter.android; then
  row "" "the DNS filter and $vpn_app both want the one VPN slot; keep one of them"; attention=1
fi

step "summary"
if [[ $attention == 1 ]]; then note "something above needs attention"; else note "nothing needs attention"; fi
exit 0
