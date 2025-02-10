README.md
# デプロイ方法
AWS EC2にデプロイするには、以下の方法で実行する。
## 1. SSHアクセス
まず、EC2にSSHアクセスして、AWSコンソールを開く。
```
ssh (.sshのconfigに書かれた情報)
```

sshコンソール内でpyenvを使ってpythonをインストールする。
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
exec "$SHELL"
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
pyenv install -l | less
pyenv install 3.11.8
pyenv versions
pyenv global 3.11.8
python -V
```

## 2. リポジトリをクローンする。
EC2にアプリケーションのリポジトリをクローンする。
git clone https://github.com/hiroya-akiba/ICS_backend.git
を実行

## 3. 環境変数ファイルを配置する。
開発環境に存在しているproduct用.envファイルとproduct用settingファイルを
このREADME.mdと同じ階層に配置する。
(※ settingsと.envはgitに置いてないので、scp等でローカルから直接送信する。)
→ デプロイツールを作成したので、以下コマンドで自動配信。
Windows : ./deploy.bat product
Linux/Mac : bash deploy.sh product

## 4. 仮想環境を構築する。
仮想環境を構築して、ライブラリインストールを行う。
```
python -m venv ICS_env
source ICS_env/bin/activate
pip install --upgrade pip setuptools
pip install -r ICS_backend/config/requirements/product/requirements.txt
```

## 5. Django
### 5.1. テスト起動
必要なライブラリのインストールが完了したら、
以下のコマンドでDjangoをテスト起動する。
```
python manage.py migrate --settings config.settings.product
python manage.py createsuperuser --settings config.settings.product
 ┗ 任意のユーザーを登録しておく
python manage.py runserver 0.0.0.0:8000 -settings config.settings.product
```
その後、適当なHTTPクライアントを用いてテストアクセスを行う。
URL : http://xx.xxx.xxx.xxx/api/inventory/login

ログイン画面のAPI結果が出力されたら問題無し。
ついでにログインできるか試しておく。

### 5.2. フォルダ作成
Staticファイルと画像ファイルを収集するフォルダを作成する。
ICS_backend/configディレクトリ配下に、staticfilesフォルダとmediaフォルダを作成する。
```
mkdir ./ICS_backend/config/staticfiles
mkdir ./ICS_backend/config/media
```
そして以下のコマンドを実行して静的ファイルを収集する。
```
python manage.py collectstatics --settings config.settings.product
```
staticfilesフォルダにcssファイルなどがコピーされてきたことを確認する。

## 6. Gunicorn
### 6.1. テスト起動
Djangoサーバーを一旦止めて、Gunicornをテスト起動する。
以下のコマンドで起動。
```
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```
再度Djangoのサーバー起動の時と同じURLでテストアクセスを行う。
この時、静的ファイルがNginxによって提供されていないため、スタイルシート等が反映されていない画面となる。

## 7. Nginx
### 7.1. テスト起動-1
Gunicornを一旦止めて、Nginxを起動する。
```
sudo apt install nginx
sudo systemctl restart nginx
```
この段階でhttp://xx.xxx.xxx.xxxにアクセスすると502 bad gatewayが表示される。

### 7.2. 設定ファイル
次に、Gunicornと連携するための設定ファイルを記載する。
```
sudo vim /etc/nginx/sites-available/project-ICS 
```
記載内容は以下。
```
server {
    listen 80;
    server_name xx.xxx.xxx.xxx;
 
    location /staticfiles/ {
        alias /home/XXX/ICS_backend/config/staticfiles/;
    }

    location /media/ {
        alias /home/XXX/ICS_backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
記載が終わったら、以下コマンドでシンボリックリンクを作成しておく。
```
sudo ln -s /etc/nginx/sites-available/project-ICS  /etc/nginx/sites-enabled/
```
### 7.3. www-dataの権限周り設定
www-data (Webサーバーのソフトウェア (NginxやApache等) がファイルシステムにアクセスするために使うユーザーアカウント) で、ICS_backendにアクセスするために、① グループに追加、② ファイル持ち主、③ 権限の書き換え を行う。
① グループへの追加
ICS_backendの権限を確認
```
ls -l /user/XXX/
drwxr-xr-x 12 XXX XXX 4096 Feb  9 13:00 /home/XXX
ls -l /user/XXX/ICS_backend
drwxr-x--- 11 XXX XXX 4096 Feb 10 14:14 /home/XXX/ICS_backend/
```
www-dataをXXXグループに追加
```
sudo usermod -aG XXX www-data
```
② ファイルの持ち主変更
```
sudo chown -R XXX:www-data /home/XXX/ICS_backend
```

③ 権限を書き換え
```
sudo chmod 755 /home/XXX
sudo chmod -R 750 /home/XXX/ICS_backend/
```

以上で、www-dataユーザーがstaticfilesにアクセスする権限を得ているかを確認する。
ローカルのターミナルから以下のコマンドを実行。
```
curl http://xx.xxx.xxx.xxx/static/rest_framework/css/bootstrap.min.css
```
この時、StatusCodeが403 や 404の時は正しく設定できていないため、どこかが間違っている。
StatusCodeが200の時、問題無く設定完了している。

最後に、適当なHTTPクライアントを用いてテストアクセスを行う。
URL : http://xx.xxx.xxx.xxx/api/inventory/login
この時に、css等が反映されていれば、静的ファイルをNginxによって提供していることが確かめられる。

