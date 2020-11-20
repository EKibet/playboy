# Generated by Django 3.1.2 on 2020-11-11 17:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0008_auto_20201028_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 24, 17, 32, 32, 874225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cohort',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 24, 17, 32, 32, 874225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
