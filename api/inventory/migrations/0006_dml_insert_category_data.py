# Generated by Django 4.2.16 on 2024-12-21 07:27
# RunSQLの方法
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    
    # dependenciesに直前のDDL操作を書く
    dependencies = [
        ("inventory", "0005_category_product_category"),
    ]

    # operationsにDML操作を書く
    operations = [
        migrations.RunSQL(
            "insert into category(name, parent_category_id) values('通常モンスター', null);",
        )
    ]