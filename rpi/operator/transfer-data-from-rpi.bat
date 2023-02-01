@echo off
set path=%cd%

"C:\Program Files (x86)\WinSCP\WinSCP.com" ^
  /ini=nul ^
  /command ^
    "open sftp://pi:rpi@192.168.0.2/ -hostkey=""ssh-ed25519 255 9NQii05JQ8SdX1qCOsjF8yWjEyO0Q+0QtCi4OtVWzm0=""" ^
    "cd pi/home/_git_code/bti-ph-2/rpi/rpi-runtime" ^
    "lcd %path%/rpi-data^
    "get *" ^
    "exit"

set WINSCP_RESULT=%ERRORLEVEL%
if %WINSCP_RESULT% equ 0 (
  echo Success
) else (
  echo Error
)

exit /b %WINSCP_RESULT%