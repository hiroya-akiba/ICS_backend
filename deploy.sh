#!/bin/bash

# カレントディレクトリをスクリプトがあるディレクトリに変更
cd "$(dirname "$0")"

echo "###############"
echo "    scp tool"
echo "###############"
echo "start date : $(date +'%Y/%m/%d %H:%M')"

thisEnvIs=$1
echo "args : $thisEnvIs"

if [ -z "$thisEnvIs" ]; then
  echo "環境変数を設定して起動してください。"
  echo "例: ./deploy.sh product"
  exit 1
elif [ "$thisEnvIs" == "product" ]; then
  echo "product環境の.envとsettingsファイルを転送します。"
elif [ "$thisEnvIs" == "staging" ]; then
  echo "staging環境の.envとsettingsファイルを転送します。"
elif [ "$thisEnvIs" == "development" ]; then
  echo "development環境の.envとsettingsファイルを転送します。"
else
  echo "環境変数は以下の3つから選択可能です。"
  echo "product / staging / development"
  exit 1
fi

echo
# .envファイルからIPアドレスを取得
gip=$(head -n 1 "./config/env/$thisEnvIs/.env" | cut -d '=' -f2)

# gipが空でない場合のみ転送処理を行う
if [ -n "$gip" ]; then
  echo "IPアドレス: $gip"

  # settings/baseファイルをscpで転送
  scp -i ~/.ssh/id_rsa "./config/settings/base.py" "hiroya@$gip:~/ICS_backend/config/settings/"

  # settingsファイルをscpで転送
  scp -i ~/.ssh/id_rsa "./config/settings/$thisEnvIs.py" "hiroya@$gip:~/ICS_backend/config/settings/"

  # .envファイルをscpで転送
  scp -i ~/.ssh/id_rsa "./config/env/$thisEnvIs/.env" "hiroya@$gip:~/ICS_backend/"
else
  echo ".envファイルからIPアドレスが取得できませんでした。転送を中止します。"
fi
