@echo off
rem Runs a dumbtv script from cmd.exe, e.g.
rem   windows\dumbtv preflight
rem   windows\dumbtv all --dry-run
rem   windows\dumbtv switch-home projectivy
rem   windows\dumbtv health
rem It hands everything to dumbtv.ps1, which finds Git Bash and adb.
rem Double-clicked with no arguments it runs the read-only health readout and waits.
setlocal
if not "%~1"=="" goto run
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0dumbtv.ps1" health
set "rc=%errorlevel%"
pause
exit /b %rc%

:run
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0dumbtv.ps1" %*
exit /b %errorlevel%
