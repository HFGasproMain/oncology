# Generated by Django 4.2.1 on 2023-07-01 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diagnosis", "0003_cancertype_treatments"),
    ]

    operations = [
        migrations.AddField(
            model_name="cancertype",
            name="symptoms",
            field=models.ManyToManyField(to="diagnosis.symptom"),
        ),
    ]
