# Generated by Django 3.1.2 on 2021-02-08 07:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0015_auto_20201128_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.date(2021, 5, 24), null=True),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.date(2021, 5, 24), null=True),
        ),
    ]
