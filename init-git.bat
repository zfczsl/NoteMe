@echo off
cd /d C:\Users\49592\WorkBuddy\20260320231952
"C:\Program Files\Git\cmd\git.exe" config --global user.name "zfczsl"
"C:\Program Files\Git\cmd\git.exe" config --global user.email "zfczsl@github.com"
"C:\Program Files\Git\cmd\git.exe" init
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Initial commit"
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/zfczsl/NoteMe.git
"C:\Program Files\Git\cmd\git.exe" push -u origin main
echo.
echo Done! 仓库已推送到 GitHub
pause
