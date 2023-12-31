# Generated by Django 4.2.1 on 2023-07-01 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diagnosis", "0006_remove_patients_test_results_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testresult",
            name="patient",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="patient_result",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
