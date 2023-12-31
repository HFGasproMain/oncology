# Generated by Django 4.2.1 on 2023-06-26 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diagnosis", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patients",
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
                ("symptoms", models.ManyToManyField(to="diagnosis.symptom")),
                ("test_results", models.ManyToManyField(to="diagnosis.testresult")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Patient",
        ),
    ]
