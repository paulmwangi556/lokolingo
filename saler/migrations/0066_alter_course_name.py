# Generated by Django 5.0 on 2024-01-02 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("saler", "0065_alter_course_date_added"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Course Name"
            ),
        ),
    ]
