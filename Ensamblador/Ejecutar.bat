@echo off
if "%~1"=="" (
    echo Escrbir el nombre de un programa sin la extension .asm
    exit /b 1
)

set PROGRAMA=%~1
if not exist "%PROGRAMA%\%PROGRAMA%.asm" (
    echo No se encontro el archivo %PROGRAMA%.asm en la carpeta %PROGRAMA%
    exit /b 1
)

cd "%PROGRAMA%"
echo --------------------
echo Creando object ...
ml /c /Zd /coff "%PROGRAMA%.asm"

echo --------------------
echo Creando ejecutable ...
link /SUBSYSTEM:CONSOLE "%PROGRAMA%.obj"

echo --------------------
echo Ejecutando ...
echo --------------------
"%PROGRAMA%.exe"
cd ..