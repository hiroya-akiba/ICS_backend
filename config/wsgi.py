"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.getenv('DJANGO_ENV', 'development') # .envで定義された環境変数で場合分け

if env == 'product':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.product')
elif env == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.staging')
elif env == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_wsgi_application()
