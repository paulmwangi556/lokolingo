# Generated by Django 4.2.7 on 2023-11-26 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saler', '0022_wholesaleproduct_prod_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_seller',
            field=models.CharField(default='', max_length=100),
        ),
    ]
