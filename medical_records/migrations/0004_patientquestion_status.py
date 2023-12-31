# Generated by Django 4.2.1 on 2023-07-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medical_records", "0003_doctorresponse"),
    ]

    operations = [
        migrations.AddField(
            model_name="patientquestion",
            name="status",
            field=models.CharField(
                choices=[("unanswered", "Unanswered"), ("answered", "Answered")],
                default="unanswered",
                max_length=20,
            ),
        ),
    ]
