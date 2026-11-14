# Runs a dumbtv script from Windows PowerShell or a double-clicked dumbtv.cmd.
# The scripts are bash; this finds Git for Windows' bash (Git Bash) and adb, then runs
# scripts/<name>.sh with the same arguments, so every flag works as on macOS and Linux.
#
#   .\windows\dumbtv.ps1 preflight
#   .\windows\dumbtv.ps1 configure
#   .\windows\dumbtv.ps1 all
#   .\windows\dumbtv.ps1 switch-home projectivy
#   .\windows\dumbtv.ps1 health
#   .\windows\dumbtv.ps1 restore --dry-run
#
# Needs Git for Windows (https://git-scm.com/download/win) and Android platform-tools
# (https://developer.android.com/tools/releases/platform-tools) with adb.exe on PATH, or
# ADB set to its full path. Pick a TV with $env:ADB_SERIAL = "<tv-ip>:5555".
# After firetv-safe-debloat's windows\*.bat by roy9611 (MIT), see CREDITS.md.
# No param() block on purpose: $args passes flags such as -y and --dry-run through
# untouched, where a declared parameter set would try to bind them itself.
$Script = if ($args.Count -gt 0) { [string]$args[0] } else { "help" }
$Rest = if ($args.Count -gt 1) { @($args[1..($args.Count - 1)] | ForEach-Object { [string]$_ }) } else { @() }
$ErrorActionPreference = "Stop"
function Fail([string] $Message, [int] $Code) { [Console]::Error.WriteLine("error: $Message"); exit $Code }
$Root = Split-Path -Parent $PSScriptRoot

# Helpers that are sourced by the others, not run.
$Internal = @("lib", "home", "accessibility", "appdata", "appui")
$Available = Get-ChildItem (Join-Path $Root "scripts") -Filter *.sh |
  ForEach-Object { $_.BaseName } | Where-Object { $Internal -notcontains $_ } | Sort-Object

if ($Script -in @("help", "-h", "--help", "/?")) {
  Write-Host "usage: dumbtv <script> [flags]   e.g. dumbtv preflight, dumbtv all --dry-run"
  Write-Host ("scripts: " + ($Available -join ", "))
  exit 0
}
$Script = $Script -replace '\.sh$', ''
if ($Available -notcontains $Script) {
  Fail ("unknown script '$Script'. One of: " + ($Available -join ", ")) 2
}

# Git Bash, not WSL's bash.exe in System32: WSL cannot reach a Windows adb.exe's server
# the same way, and its paths differ.
$Candidates = @()
if ($env:DUMBTV_BASH) { $Candidates += $env:DUMBTV_BASH }
foreach ($base in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA)) {
  if ($base) {
    $Candidates += (Join-Path $base "Git\bin\bash.exe")
    $Candidates += (Join-Path $base "Programs\Git\bin\bash.exe")
  }
}
$git = Get-Command git.exe -ErrorAction SilentlyContinue
if ($git) { $Candidates += (Join-Path (Split-Path -Parent (Split-Path -Parent $git.Source)) "bin\bash.exe") }
$Bash = $Candidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $Bash) {
  Fail "Git Bash not found. Install Git for Windows (https://git-scm.com/download/win), or set DUMBTV_BASH to its bash.exe." 1
}

if (-not $env:ADB) {
  $adb = Get-Command adb.exe -ErrorAction SilentlyContinue
  if (-not $adb) {
    Fail "adb.exe not found. Install Android platform-tools and add its folder to PATH, or set ADB to adb.exe's full path." 1
  }
  $env:ADB = $adb.Source
}
# bash wants forward slashes; adb.exe takes them too.
$env:ADB = $env:ADB -replace '\\', '/'

$Target = (Join-Path $Root "scripts\$Script.sh") -replace '\\', '/'
& $Bash $Target @Rest
exit $LASTEXITCODE
