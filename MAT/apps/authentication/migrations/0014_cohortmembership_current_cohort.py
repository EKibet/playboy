# Generated by Django 3.0.6 on 2020-10-06 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_auto_20201006_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohortmembership',
            name='current_cohort',
            field=models.BooleanField(null=True),
        ),
    ]
