# Generated by Django 5.0.3 on 2024-03-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("performace_test", "0003_remove_performacetestsuite_jrampup_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="testcontainersruns",
            name="raw_data",
            field=models.JSONField(null=True),
        ),
    ]
