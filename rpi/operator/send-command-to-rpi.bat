@echo off

"C:\Program Files (x86)\WinSCP\WinSCP.com" ^
  /ini=nul ^
  /command ^
    "open sftp://pi:rpi@10.1.10.88/ -hostkey=""ssh-ed25519 255 9NQii05JQ8SdX1qCOsjF8yWjEyO0Q+0QtCi4OtVWzm0=""" ^
    "cd /home/pi/Codesys" ^
    "lcd C:\Users\matth\OneDrive\Documents" ^
    "get *" ^
    "exit"

set WINSCP_RESULT=%ERRORLEVEL%
if %WINSCP_RESULT% equ 0 (
  echo Success
) else (
  echo Error
)

exit /b %WINSCP_RESULT%