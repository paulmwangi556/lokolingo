# Generated by Django 5.0 on 2023-12-17 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saler', '0041_remove_booking_status_remove_booking_tutor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='message',
            new_name='student_message',
        ),
        migrations.AddField(
            model_name='booking',
            name='tutor_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
