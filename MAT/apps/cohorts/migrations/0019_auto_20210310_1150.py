# Generated by Django 3.1.2 on 2021-03-10 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0018_merge_20210302_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.date(2021, 6, 23), null=True),
        ),
        migrations.AlterField(
            model_name='historicalcohort',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.date(2021, 6, 23), null=True),
        ),
    ]