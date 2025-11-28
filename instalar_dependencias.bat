@echo off
echo Instalando dependencias do projeto...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro ao instalar as dependencias.
    pause
    exit /b %errorlevel%
)
echo.
echo Dependencias instaladas com sucesso!
pause
