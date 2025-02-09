from common.migrate_util import common_load_fixture
from django.conf import settings
from django.core.management import call_command
from django.db import migrations

def load_fixture(apps, schema_editor):
    common_load_fixture(__file__) # この関数が実行されている絶対パスが__file__に代入され、
    # common_load_fixtureの実装で、settingsファイルによる分別が行われるため、
    # 環境によって読み込むfixtureファイルを変えることが可能
    # 条件として、settingsファイルのファイル名と、fixtureのファイル名を揃えることが必要
    # 例) config/settings/product.py を使用してmigrationを行う場合
    #     (python manage.py migration --settings config.settings.product)
    #     は、0011_dml_insert_product_data_by_fixture_environment/product.yaml
    #     が読み込まれる。

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_dml_insert_category_data_by_fixture_environment'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]