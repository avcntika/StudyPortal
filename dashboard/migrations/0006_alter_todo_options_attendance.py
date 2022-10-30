# Generated by Django 4.1.2 on 2022-10-19 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dashboard", "0005_todo"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="todo", options={"verbose_name_plural": "To Do List"},
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Class", models.CharField(max_length=100)),
                ("lectures_conducted", models.CharField(max_length=10)),
                ("lectures_attended", models.CharField(max_length=10)),
                ("attendance_percentage", models.CharField(max_length=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "Attendance",},
        ),
    ]