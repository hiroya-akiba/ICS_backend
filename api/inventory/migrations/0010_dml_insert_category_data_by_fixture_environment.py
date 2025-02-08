# manage.pyを用いずにfixtureを使用する方法
# 1. 呼び出すファイル元 (このマイグレーションファイル) を作成
# 2. loaddataを実行するファイル (/common/migrate_util.py) を作成
# 3. マイグレーションファイルで読み込めるファイル名 (base.yaml) のfixtureファイルを作成

from common.migrate_util import common_load_fixture
from django.conf import settings
from django.core.management import call_command
from django.db import migrations

def load_fixture(apps, schema_editor):
    common_load_fixture(__file__) # この関数が実行されている絶対パスが__file__に代入される
    # __で囲われた変数・メソッドを特殊メソッドと呼ぶ

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_dml_insert_category_data_by_fixture'),
    ]


    operations = [
        migrations.RunPython(load_fixture),
    ]