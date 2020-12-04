# Generated by Django 3.0.6 on 2020-10-06 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cohorts', '0002_historicalcohort'),
        ('authentication', '0012_auto_20200910_1242'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # Old table name from checking with sqlmigrate, new table
                # name from AuthorBook._meta.db_table.
                migrations.RunSQL(
                    sql='ALTER TABLE authentication_user_cohort RENAME TO authentication_cohortmembership',
                    reverse_sql='ALTER TABLE authentication_cohortmembership RENAME TO authentication_user_cohort',
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name='CohortMembership',
                    fields=[
                        ('id', models.AutoField(auto_created=True,
                                                primary_key=True, serialize=False, verbose_name='ID')),
                        ('cohort', models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE, to='cohorts.Cohort')),
                        ('user', models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                ),
                migrations.AlterField(
                    model_name='user',
                    name='cohort',
                    field=models.ManyToManyField(blank=True, related_name='members',
                                                 through='authentication.CohortMembership', to='cohorts.Cohort'),
                ), ])
    ]