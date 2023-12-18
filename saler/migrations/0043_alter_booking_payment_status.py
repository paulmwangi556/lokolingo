# Generated by Django 5.0 on 2023-12-17 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saler', '0042_rename_message_booking_student_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('payment_not_initiated', 'Payment Not Initiated'), ('payment_initiated', 'Payment Initiated'), ('payment_pending', 'Payment Pending'), ('payment_completed', 'Payment Completed'), ('payment_failed', 'Payment Failed')], default='payment_not_initiated', max_length=30),
        ),
    ]
