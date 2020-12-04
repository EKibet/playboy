# Generated by Django 3.1.2 on 2020-11-11 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0009_auto_20201111_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='end_date',
            field=models.DateField(default=datetime.date(2021, 2, 24)),
        ),
        migrations.AlterField(
            model_name='cohort',
            name='start_date',
            field=models.DateField(default=datetime.date(2020, 11, 11)),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='end_date',
            field=models.DateField(default=datetime.date(2021, 2, 24)),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='start_date',
            field=models.DateField(default=datetime.date(2020, 11, 11)),
        ),
    ]