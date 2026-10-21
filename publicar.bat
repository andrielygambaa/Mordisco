@echo off
title Mordisco - Publicar no GitHub
cd /d "%~dp0"

echo.
echo  ==============================================
echo    MORDISCO :: publicar no GitHub
echo  ==============================================
echo.
echo  Antes de comecar, crie o repositorio vazio no site:
echo  https://github.com/new
echo  ^- Nome: mordisco
echo  ^- NAO marque "Add a README file" nem ".gitignore"
echo  ^- Porque esse projeto ja tem os dois.
echo.

REM ---------- 1. Identidade (o nome que aparece no commit) ----------
set NOME=
set /p NOME="Seu nome no GitHub [Andriely Gamba]: "
if not defined NOME set NOME=Andriely Gamba

set EMAIL=
set /p EMAIL="Seu e-mail do GitHub [andriely.gamba@email.com]: "
if not defined EMAIL set EMAIL=andriely.gamba@email.com

git config user.name "%NOME%"
git config user.email "%EMAIL%"

REM ---------- 2. Usuario e nome do repositorio ----------
set USUARIO=
set /p USUARIO="Seu usuario do GitHub, sem o arroba: "
if not defined USUARIO (
  echo.
  echo  Preciso do seu usuario do GitHub para montar o link.
  pause
  exit /b 1
)

set REPO=mordisco
set NOME_REPO=
set /p NOME_REPO="Nome do repositorio [mordisco]: "
if defined NOME_REPO set REPO=%NOME_REPO%

REM ---------- 3. Conectar com o repositorio ----------
echo.
echo  Conectando com o GitHub...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%USUARIO%/%REPO%.git
git remote -v

REM ---------- 4. Salvar e enviar ----------
echo.
echo  Salvando as alteracoes...
git add -A
git commit -m "Mordisco: sistema web de estoque da cantina (Atividade 3)" >nul 2>&1

echo  Enviando para o GitHub...
echo  ^(pode abrir uma janela do navegador para voce entrar no GitHub^)
echo.
git push -u origin main

if errorlevel 1 (
  echo.
  echo  [X] Nao foi possivel publicar.
  echo      Veja as mensagens acima. O mais comum e:
  echo      - o repositorio ainda nao existe no site (crie em https://github.com/new)
  echo      - o nome do usuario esta errado
  echo      - voce recusou o login que o navegador pediu
  echo.
  pause
  exit /b 1
)

echo.
echo  ==============================================
echo   PRONTO! Seu projeto esta no GitHub.
echo  ==============================================
echo.
echo  https://github.com/%USUARIO%/%REPO%
echo.
start "" "https://github.com/%USUARIO%/%REPO%"
pause
