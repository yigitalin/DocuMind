@echo off
cd /d "C:\Users\user\Desktop\DocuMind"
call venv\Scripts\activate.bat
venv\Scripts\python.exe -m uvicorn app.main:app --reload
pause