# Generated by Django 5.0.3 on 2024-03-26 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("performace_test", "0002_jmetertestconfig_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="performacetestsuite",
            name="jrampup",
        ),
        migrations.RemoveField(
            model_name="performacetestsuite",
            name="jthreads",
        ),
        migrations.AddField(
            model_name="performacetestsuite",
            name="durations",
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name="performacetestsuite",
            name="jrampup_steps",
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name="performacetestsuite",
            name="jrampup_time",
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name="performacetestsuite",
            name="jthreads_total_user",
            field=models.CharField(blank=True, default="1", max_length=250, null=True),
        ),
    ]
