@echo off

"C:\Users\HelloWorld\AppData\Local\Programs\WinSCP\WinSCP.com" ^
  /command ^
    "open sftp://pi:rpi@192.168.0.241/ -hostkey=""ssh-ed25519 255 F90yjkDmQFFmfLMxje5x/IbnnmdNwCQBLXEC0dZQLlM""" ^
    "cd /home/pi/git_code/bti-ph-2/rpi/rpi-runtime" ^
    "lcd C:\Users\HelloWorld\Documents\_git_code\bti-ph-2\rpi\operator\rpi-data" ^
    "get -neweronly *" ^
    "exit"

set WINSCP_RESULT=%ERRORLEVEL%
if %WINSCP_RESULT% equ 0 (
  echo Success
) else (
  echo Error
)

exit /b %WINSCP_RESULT%