# Generated by Django 5.0 on 2024-01-05 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("saler", "0002_remove_bookingpayments_booking_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookingpayments",
            name="content_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="contenttypes.contenttype",
            ),
        ),
    ]
