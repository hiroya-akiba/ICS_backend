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
git clone https://github.com/hiroya-akiba/ICS_backend.git
を実行

## 3. 環境変数ファイルを配置する。
ローカルのproduct用.envファイルとproduct用settingファイルを
このREADME.mdと同じ階層に配置する。
(※ .envはgitに置いてないので、scp等でローカルから直接送信する。)
→ デプロイツールを作成したので、以下コマンドを実行する。
Windows : ./deploy.bat product
Linux/Mac : bash deploy.sh product

## 4. 仮想環境を構築する。
仮想環境を構築して、ライブラリインストールを行う。
```
python -m venv ICS_env
source ICS_env/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

## 5. Djangoをテスト起動
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

## 6. Gunicornをテスト起動
Djangoサーバーを一旦止めて、Gunicornをテスト起動する。
以下のコマンドで起動。
```
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```
再度Djangoのサーバー起動の時と同じURLでテストアクセスを行う。

## 7. 