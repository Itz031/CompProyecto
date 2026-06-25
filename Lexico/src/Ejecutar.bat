@echo off
if "%~1"=="" (
    echo Uso correcto: doMain.bat NombrePrograma
    exit /b 1
)
python "%~1.py" archivo_codigo.txt