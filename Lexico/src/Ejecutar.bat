@echo off
if "%~1"=="" (
    echo Uso correcto: Ejecutar.bat nombre_del_archivo.c
    exit /b 1
)

echo 
python Main.py "%~1"