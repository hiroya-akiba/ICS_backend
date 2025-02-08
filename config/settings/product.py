from .base import  *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'app_product'),  # 環境変数から取得
        'USER': os.getenv('MYSQL_USER', 'admin'),  # 環境変数から取得
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'hiroya168'),  # 環境変数から取得
        'HOST': os.getenv('MYSQL_HOST', 'ics-mysql.cdqm4iwostvx.ap-northeast-1.rds.amazonaws.com'),  # AWS RDSのエンドポイント
        'PORT': os.getenv('MYSQL_PORT', '3306'),  # RDSのポート（通常は3306）
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'charset': 'utf8mb4',  # 文字コード設定（絵文字対応）
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  # 厳格モード
        },
    }
}