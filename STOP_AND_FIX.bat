@echo off
echo Parando aplicacao...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Criando usuario admin...
python fix_login.py

echo.
echo Aplicacao pronta! Execute: python app.py
pause
