# Running dumbtv from Windows

The scripts are bash. On Windows they run in Git Bash, and these two files spare you
opening it: `dumbtv.cmd` for cmd.exe or a double-click, `dumbtv.ps1` for PowerShell.
Both run `scripts/<name>.sh` with the flags you give, unchanged.

You need:

1. [Git for Windows](https://git-scm.com/download/win) (it brings Git Bash).
2. [Android platform-tools](https://developer.android.com/tools/releases/platform-tools),
   with the folder holding `adb.exe` on your PATH, or `ADB` set to its full path.

Then, from the repository folder:

```bat
adb connect <tv-ip>:5555
windows\dumbtv preflight
windows\dumbtv configure
windows\dumbtv all --dry-run
windows\dumbtv all
windows\dumbtv verify
windows\dumbtv switch-home projectivy
windows\dumbtv health
windows\dumbtv restore
```

`windows\dumbtv help` lists every script. Double-clicking `dumbtv.cmd` runs the
read-only `health` readout and waits for a key.

With more than one TV connected, pick one first: `set ADB_SERIAL=<tv-ip>:5555` in
cmd.exe, `$env:ADB_SERIAL = "<tv-ip>:5555"` in PowerShell. `dumbtv.conf` and `report/`
describe one household and one TV; for a second TV, point `CONF` and `REPORT` at its
own files, written with forward slashes for bash: `set CONF=C:/dumbtv/living-room.conf` and
`set REPORT=C:/dumbtv/report/living-room`.

Git Bash is found in the usual install folders or next to `git.exe`; set `DUMBTV_BASH`
to a `bash.exe` to use another. WSL's `bash.exe` is not used: from WSL, run the
scripts directly with Linux's adb instead.

PowerShell may refuse to run a downloaded script; `dumbtv.cmd` passes
`-ExecutionPolicy Bypass` for this one file only. From a PowerShell prompt, use
`powershell -ExecutionPolicy Bypass -File windows\dumbtv.ps1 <script>`, or
`Unblock-File windows\dumbtv.ps1` once.
