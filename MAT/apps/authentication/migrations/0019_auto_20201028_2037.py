# Generated by Django 3.1.2 on 2020-10-28 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_merge_20201028_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='is_podleader',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_podleader',
        ),
    ]
