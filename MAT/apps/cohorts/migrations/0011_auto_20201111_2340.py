# Generated by Django 3.1.2 on 2020-11-11 20:40

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0010_auto_20201111_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 24, 20, 40, 37, 244203, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cohort',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 24, 20, 40, 37, 244203, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]