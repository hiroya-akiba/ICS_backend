from .base import  *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_product', #Databaseの名前が記載されている
        'USER': 'root', #ログイン情報 ID
        'PASSWORD': 'password', #ログイン情報 PASS
        'HOST': 'host.docker.internal',
        'PORT': '53306',
        'ATOMIC_REQUESTS': True
    }
}