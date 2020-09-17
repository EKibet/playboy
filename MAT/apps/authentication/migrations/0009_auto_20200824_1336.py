# Generated by Django 3.0.6 on 2020-08-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0002_historicalcohort'),
        ('authentication', '0008_auto_20200227_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='cohort',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cohort',
        ),
        migrations.AddField(
            model_name='user',
            name='cohort',
            field=models.ManyToManyField(related_name='members', to='cohorts.Cohort'),
        ),
    ]
