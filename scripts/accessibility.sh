#!/usr/bin/env bash
# Read-only parser for the bound-service section of dumpsys accessibility.
# Android 9 calls it "services"; newer Android calls it "Bound services".
# AOSP prints the service label, not its component, in these sections. Keep the
# label in sync with launcher/res/values/strings.xml. Right after the APK is
# updated, Android 9 prints the class name in place of the label until the
# resources load, so that form counts as bound too. Enabled components are
# checked separately by verify.sh. This is a health check, not an identity proof.
# Return 0 = bound, 1 = a recognized empty/other-service section, 2 = unknown.
# $2 = projectivy checks Projectivy Launcher's service instead of dumbtv home's Guard.
guard_bound() {
  awk -v wanted="$1" -v which="${2:-dumbtv}" '
    /User state\[/ { user = ""; inside = 0 }
    /attributes:\{id=[0-9]+[,}]/ {
      id = $0
      sub(/^.*attributes:\{id=/, "", id)
      sub(/[,}].*$/, "", id)
      user = id
    }
    user == wanted && /^[[:space:]]*(Bound services|services):[[:space:]]*\{/ {
      inside = 1
      sub(/^[^{]*\{/, "")
    }
    inside {
      # Never accept a similarly named service or a label in Enabled/Binding.
      if (which == "dumbtv" && index($0, "Service[label=dumbtv home button,")) found = 1
      if (which == "dumbtv" && index($0, "Service[label=tv.dumbtv.home.Guard,")) found = 1
      # Projectivy names its service in its own language; its class name stands in
      # while resources load, as for the Guard above.
      if (which == "projectivy" && index($0, "Service[label=Projectivy")) found = 1
      if (which == "projectivy" && index($0, "Service[label=com.spocky.projengmenu.services.ProjectivyAccessibilityService,")) found = 1
      if (index($0, "}")) { seen = 1; inside = 0 }
    }
    END { if (!seen || inside) exit 2; exit (found ? 0 : 1) }
  '
}
