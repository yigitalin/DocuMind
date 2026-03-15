@echo off
cd /d "C:\Users\user\Desktop\DocuMind"
start "" "C:\Users\user\AppData\Local\Programs\Ollama\ollama.exe"
timeout /t 3 /nobreak
call venv\Scripts\activate.bat
start "" "%cd%\frontend\index.html"
venv\Scripts\python.exe -m uvicorn app.main:app --reload
pause