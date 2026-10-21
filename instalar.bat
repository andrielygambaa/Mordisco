@echo off
chcp 65001 >nul
title Mordisco - Preparar ambiente
cd /d "%~dp0"

echo.
echo  ==============================================
echo    MORDISCO :: preparando o ambiente
echo  ==============================================
echo.
echo  Isso so precisa ser feito UMA VEZ.
echo  Depois, e so dar dois cliques no iniciar.bat
echo.

REM ==========================================================
REM  1. Descobrir qual Python usar
REM ==========================================================
set PY=
python --version >nul 2>&1
if not errorlevel 1 set PY=python

if not defined PY (
  py --version >nul 2>&1
  if not errorlevel 1 set PY=py
)

REM ----- procura o Python nos lugares onde ele costuma ficar -----
if not defined PY (
  for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%~fD\python.exe" set PY="%%~fD\python.exe"
)
if not defined PY (
  for /d %%D in ("%ProgramFiles%\Python3*") do if exist "%%~fD\python.exe" set PY="%%~fD\python.exe"
)
if not defined PY (
  for /d %%D in ("C:\Python3*") do if exist "%%~fD\python.exe" set PY="%%~fD\python.exe"
)

if not defined PY (
  echo  [X] Python nao foi encontrado neste computador.
  echo.
  echo      Baixe em https://www.python.org/downloads/
  echo      e marque "Add Python to PATH" na instalacao.
  echo.
  pause
  exit /b 1
)

REM ==========================================================
REM  2. Criar o ambiente virtual
REM ==========================================================
if exist ".venv\Scripts\python.exe" (
  echo  Ambiente virtual ja existe. Pulando esta etapa.
) else (
  echo  [1/2] Criando o ambiente virtual na pasta .venv...
  %PY% -m venv .venv
  if not exist ".venv\Scripts\python.exe" (
    echo  [X] Falha ao criar o ambiente virtual.
    pause
    exit /b 1
  )
)

REM ==========================================================
REM  3. Instalar as dependencias - Flask e Flask-Cors
REM ==========================================================
echo  [2/2] Instalando Flask e Flask-Cors...
echo  Pode demorar um pouco na primeira vez.
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
  echo  [X] Falha ao instalar as dependencias. Confira a internet e tente de novo.
  pause
  exit /b 1
)

echo.
echo  Pronto! Agora e so dar dois cliques no iniciar.bat
echo  ou abrir esta pasta e executar o iniciar.bat.
echo.
pause
