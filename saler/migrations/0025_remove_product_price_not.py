# Generated by Django 4.2.7 on 2023-11-27 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saler', '0024_remove_salerdetail_shop_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_not',
        ),
    ]
