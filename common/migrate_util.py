# fixutreファイルを読み込む実装メソッド
import os

from django.conf import settings
from django.core.management import call_command

def common_load_fixture(migration_filename):
    setting_file = settings.SETTINGS_MODULE
    env_name = setting_file.split('.')[-1]
    target = os.path.splitext(migration_filename)[0].replace('migrations', 'fixtures')
    base_yaml_name = target + '/base.yaml'
    env_yaml_name  = target + '/' + env_name + '.yaml'

    # 環境で共通のfixutreファイル
    if os.path.isfile(base_yaml_name):
        call_command('loaddata', '--settings', setting_file, '--format=yaml', base_yaml_name)

    # 環境別のfixtureファイル
    if os.path.isfile(env_yaml_name):
        call_command('loaddata', '--settings', setting_file, '--format=yaml', env_yaml_name)