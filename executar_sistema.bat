@echo off
echo Iniciando o Sistema de Gestao...
python tela_inicial.py
if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro ao executar o sistema.
    pause
    exit /b %errorlevel%
)
pause
