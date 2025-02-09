@echo off
REM カレントディレクトリをスクリプトがあるディレクトリに変更
cd /d "%~dp0"

echo ###############
echo     scp tool
echo ###############
echo start date : %date% %time%

REM 引数を変数に格納
set thisEnvIs=%1
echo args : %thisEnvIs%

REM 引数が空かどうかチェック
if "%thisEnvIs%"=="" (
  echo 環境変数を設定して起動してください。
  echo 例: deploy.bat product
  exit /b 1
)

REM 引数に基づいて環境を選択
if "%thisEnvIs%"=="product" (
  echo product環境の.envとsettingsファイルを転送します。
) else if "%thisEnvIs%"=="staging" (
  echo staging環境の.envとsettingsファイルを転送します。
) else if "%thisEnvIs%"=="development" (
  echo development環境の.envとsettingsファイルを転送します。
) else (
  echo 環境変数は以下の3つから選択可能です。
  echo product / staging / development
  exit /b 1
)

echo

REM .envファイルからIPアドレスを取得
set gip=
for /f "tokens=2 delims==" %%A in ('findstr /r "^.*=" .\config\env\%thisEnvIs%\ .env') do set gip=%%A

REM gipが空でない場合のみ転送処理を行う
if not "%gip%"=="" (
  echo IPアドレス: %gip%

  REM settingsファイルをscpで転送
  pscp -i C:\Users\hiroya\.ssh\id_rsa .\config\settings\%thisEnvIs%.py hiroya@%gip%:~/ICS_backend/config/settings/

  REM .envファイルをscpで転送
  pscp -i C:\Users\hiroya\.ssh\id_rsa .\config\env\%thisEnvIs%\.env hiroya@%gip%:~/ICS_backend/
) else (
  echo .envファイルからIPアドレスが取得できませんでした。転送を中止します。
)