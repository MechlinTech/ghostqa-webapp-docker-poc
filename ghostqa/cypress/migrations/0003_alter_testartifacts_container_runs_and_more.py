# Generated by Django 5.0.2 on 2024-02-23 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cypress", "0002_testcontainersruns_testartifacts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testartifacts",
            name="container_runs",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs_artifacts",
                to="cypress.testcontainersruns",
            ),
        ),
        migrations.AlterField(
            model_name="testartifacts",
            name="suite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="suite_artifacts",
                to="cypress.testsuite",
            ),
        ),
        migrations.AlterField(
            model_name="testcontainersruns",
            name="suite",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="container_runs",
                to="cypress.testsuite",
            ),
        ),
    ]
