@echo off
if "%~1"=="" (
    echo Uso: doMain.bat codigo.c
    exit /b 1
)

set NOMBRE_BASE=%~n1
echo COMPILANDO PYTHON A MASM...
python Main.py "%~1"
if not exist "%NOMBRE_BASE%.asm" exit /b 1

echo ENSAMBLANDO CON MASM32...
:: Usamos la ruta completa hacia ml.exe
C:\masm32\bin\ml.exe /c /Zd /coff "%NOMBRE_BASE%.asm"
if errorlevel 1 exit /b 1

echo ENLAZANDO...
:: Usamos la ruta completa hacia link.exe
C:\masm32\bin\link.exe /SUBSYSTEM:CONSOLE "%NOMBRE_BASE%.obj"
if errorlevel 1 exit /b 1

echo EJECUTANDO...
"%NOMBRE_BASE%.exe"