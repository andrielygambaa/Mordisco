@echo off
chcp 65001 >nul
title Mordisco - Estoque da Cantina
cd /d "%~dp0"

echo.
echo  ==============================================
echo    MORDISCO  ::  Estoque da Cantina
echo  ==============================================
echo.

REM ==========================================================
REM  1. Descobrir qual Python usar
REM     - se o ambiente (.venv) ja existe, ele ja tem o Python
REM     - senao, procura o Python instalado no computador
REM ==========================================================
if exist ".venv\Scripts\python.exe" (
  set PY=".venv\Scripts\python.exe"
) else (
  set PY=
  python --version >nul 2>&1
  if not errorlevel 1 set PY=python
  if not defined PY (
    py --version >nul 2>&1
    if not errorlevel 1 set PY=py
  )

  if not defined PY (
    echo  [X] Python nao foi encontrado neste computador.
    echo.
    echo      Baixe o Python em https://www.python.org/downloads/
    echo      e, ao instalar, marque a opcao "Add Python to PATH".
    echo.
    pause
    exit /b 1
  )

  REM ----- primeira execucao: prepara o ambiente -----
  echo  Primeira execucao: preparando o ambiente do projeto...
  echo  ^(precisa de internet so nesta etapa^)
  echo.
  call "%~dp0instalar.bat"
  if not exist ".venv\Scripts\python.exe" (
    echo  [X] Nao foi possivel preparar o ambiente.
    pause
    exit /b 1
  )
)

REM ==========================================================
REM  2. Abrir o navegador assim que o servidor subir
REM ==========================================================
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:5000'"

REM ==========================================================
REM  3. Rodar a aplicacao
REM ==========================================================
echo  Subindo o servidor em http://localhost:5000
echo  Para parar, feche esta janela ou aperte CTRL + C.
echo.
".venv\Scripts\python.exe" app.py

echo.
echo  O servidor foi encerrado. Ate a proxima!
pause
