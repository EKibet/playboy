# Generated by Django 3.0.3 on 2020-02-11 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='active',
            new_name='is_active',
        ),
    ]
