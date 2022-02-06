@echo off
set /p username="Enter your MS account username: "
set /p password="Enter your MS account password: "
robot -v username:%username% -v password:%password% -v browser:Chrome -v desktop_count:1 -v mobile_count:20 -d results -L DEBUG tests/main.robot
pause