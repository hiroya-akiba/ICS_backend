# Generated by Django 4.2.16 on 2024-12-21 07:27
# RunPythonの方法
from django.db import migrations, models
import django.db.models.deletion

# 自動的に関連する引数が渡される
# args[0] apps: migrationに関連するモデルの情報 
# args[1] schema_editor: データベースの変更や実行を管理するインスタンス
def insert_category(apps, schema_editor):
    Category = apps.get_model('inventory', 'Category')
    Category.objects.create(name='effective monster', parent_category=None)

class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0006_dml_insert_category_data"),
    ]
    
    # RunPython…マイグレーションファイル内で様々なpythonコマンドを実行する
    operations = [
        migrations.RunPython(insert_category),
    ]