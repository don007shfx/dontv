#!/usr/bin/env bash
# Puts back only what a Fire OS update (or anything else) undid since the last pass:
# listed packages that are on again, privacy and opt-in settings that drifted, never-disable
# packages that are off, and, when they were set up, the lockdown and the DNS filter's
# always-on VPN. Nothing that is still as dontv left it is touched. Shows the plan first
# and asks unless -y; --dry-run changes nothing. No reboot.
# After couch-tv's daily repair (tv-home/tools, MIT, Seagey; see CREDITS.md), run by hand
# instead of from a computer left on.
# Usage: ./scripts/repair.sh [--dry-run] [-y]
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
parse_flags "$@"
need_device
need_supported_fireos
load_conf
check_keep_list

LOG="$REPORT/debloat.txt"
installed=$(dev 'pm list packages' | tr -d '\r' | sed -n 's/^package://p')
off=$(dev 'pm list packages -d' | tr -d '\r' | sed -n 's/^package://p')
has() { grep -qxF "$1" <<<"$2"; }

# Packages: this TV's record when there is one (what the last pass disabled), else the lists.
ours=""
if report_is_ours "$LOG"; then
  ours=$(awk -F'\t' '$2 == "disabled" {print $1}' "$LOG")
  source_note="${LOG#"$ROOT"/} (the last pass on this TV)"
else
  ours=$(cleanup_list)
  source_note="the lists (no record of a pass on this TV in ${LOG#"$ROOT"/})"
fi
protected_list=$(list_of "$(fos protected.txt)")
load_boot_homes
back=""
for p in $ours; do
  protected_by_policy "$p" && continue
  keep_pkg "$p" && continue
  has "$p" "$protected_list" && continue
  has "$p" "$installed" || continue
  has "$p" "$off" && continue
  boot_needed "$p" && continue
  back="$back $p"
done
needed=""
for p in $(list_of "$(fos never-disable.txt)" | awk '{print $1}'); do
  has "$p" "$off" || continue
  dev "dumpsys package $p" | grep -q 'User 0:.* enabled=3 ' || continue
  needed="$needed $p"
done

# Settings: privacy keys, and the opt-in tweaks that are on.
current=$(dev 'settings list secure; settings list global; settings list system' | tr -d '\r')
value_of() { printf '%s\n' "$current" | awk -v k="$1" 'index($0, k "=") == 1 { print substr($0, length(k) + 2); exit }'; }
drift=()
while read -r ns key value; do
  [[ -z ${ns:-} ]] && continue
  [[ $(value_of "$key") == "$value" ]] || drift+=("$ns $key $value")
done < <(settings_files | sed 's/ = / /')
optdrift=()
while read -r _ state file; do
  [[ $state == on ]] || continue
  while read -r ns key value; do
    [[ $(value_of "$key") == "$value" ]] || optdrift+=("$ns $key $value")
  done < <(list_of "$file")
done < <(optin_tweaks)

# Lockdown: set up when Data Saver is on or a lockdown record names this TV; drifted when a
# present protected package's uid is missing from the metered-data blacklist.
lock_fix=0
saver=$(dev 'cmd netpolicy get restrict-background' | tr -d '\r')
if [[ $saver == *enabled* ]] || report_is_ours "$REPORT/lockdown.txt"; then
  black=$(dev 'cmd netpolicy list restrict-background-blacklist' | tr -d '\r')
  [[ $saver == *enabled* ]] || lock_fix=1
  for p in $protected_list; do
    keep_pkg "$p" && continue
    has "$p" "$installed" || continue
    uid=$(uid_of "$p")
    [[ -n $uid && $uid -ge 10000 ]] || continue
    grep -qw "$uid" <<<"$black" || lock_fix=1
  done
fi

# DNS filter: set up when DNSFILTER=1 and personalDNSfilter is installed. Another VPN app
# (Proton VPN, say) owns the slot, so then the filter is left alone.
dns_fix=""
if [[ $DNSFILTER == 1 ]] && has dnsfilter.android "$installed"; then
  vpn_app=$(other_vpn_app)
  if [[ -n $vpn_app ]]; then
    dns_note="left alone: $vpn_app holds the VPN slot"
  else
    has dnsfilter.android "$off" && dns_fix="enable"
    [[ $(value_of always_on_vpn_app) == dnsfilter.android ]] || dns_fix="${dns_fix:+$dns_fix }always-on"
  fi
fi

step "plan"
note "compared with $source_note"
note "packages on again   ${back:- none}"
note "needed, but off     ${needed:- none}"
note "settings drifted    ${#drift[@]} privacy, ${#optdrift[@]} opt-in"
note "lockdown            $([[ $lock_fix == 1 ]] && echo "re-apply" || echo "as set (or not set up)")"
note "dns filter          ${dns_note:-${dns_fix:-as set (or not set up)}}"
if [[ -z $back && -z $needed && ${#drift[@]} == 0 && ${#optdrift[@]} == 0 && $lock_fix == 0 && -z $dns_fix ]]; then
  note "nothing drifted; nothing to do"
  exit 0
fi
if [[ $DRY_RUN == 0 ]]; then
  confirm "Put these back on $SERIAL?" || die "cancelled"
fi

step "packages"
for p in $back; do
  out=$(acmd pm disable-user --user 0 "$p" | head -1)
  printf '  %-46s %s\n' "$p" "${out:-disabled}"
done
for p in $needed; do
  out=$(acmd pm enable --user 0 "$p" | head -1)
  printf '  %-46s %s\n' "$p" "${out:-enabled}"
done
[[ -n $back || -n $needed ]] || note "none"

step "settings"
for line in ${drift[@]+"${drift[@]}"}; do
  read -r ns key value <<<"$line"
  acmd settings put "$ns" "$key" "$value" >/dev/null
  printf '  %-46s %s\n' "$key" "$value"
done
for line in ${optdrift[@]+"${optdrift[@]}"}; do
  read -r ns key value <<<"$line"
  optin_apply "$ns" "$key" "$value"
  printf '  %-46s %s (opt-in)\n' "$key" "$value"
done
[[ ${#drift[@]} -gt 0 || ${#optdrift[@]} -gt 0 ]] || note "none"

if [[ $lock_fix == 1 ]]; then
  step "lockdown"
  flags=(-y); [[ $DRY_RUN == 1 ]] && flags+=(--dry-run)
  ADB=$ADB ADB_SERIAL=$SERIAL REPORT=$REPORT CONF=$CONF "$ROOT/scripts/lockdown.sh" "${flags[@]}" | sed 's/^/  /'
fi

if [[ -n $dns_fix ]]; then
  step "dns filter"
  if [[ $dns_fix == *enable* ]]; then
    acmd pm enable --user 0 dnsfilter.android >/dev/null
    note "personalDNSfilter enabled again"
  fi
  # Taking the VPN slot can drop a network adb session for a moment.
  acmd settings put secure always_on_vpn_app dnsfilter.android >/dev/null
  note "always-on VPN: dnsfilter.android"
  [[ $DRY_RUN == 1 ]] || { sleep 3; adb_reconnect; }
fi

step "summary"
[[ $DRY_RUN == 1 ]] && { note "dry-run: nothing was changed"; exit 0; }
note "repaired; ./scripts/verify.sh checks the result, ./scripts/health.sh shows the rest"
