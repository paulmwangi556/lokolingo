# Generated by Django 5.0 on 2023-12-17 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saler', '0044_booking_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='duration',
            field=models.CharField(default='1', max_length=5),
        ),
    ]
