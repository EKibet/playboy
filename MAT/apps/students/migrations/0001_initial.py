
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, help_text='This is to make sure deletes are not actual deletes')),
                ('is_active', models.BooleanField(default=True)),
                ('is_present', models.BooleanField(default=False)),
                ('is_late', models.BooleanField(default=True)),
                ('checked_in', models.DateTimeField(null=True)),
                ('is_checked_in', models.BooleanField(default=False)),
                ('is_checked_out', models.BooleanField(default=False)),
                ('checked_out', models.DateTimeField(null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
                'abstract': False,
            },
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, help_text='This is to make sure deletes are not actual deletes')),
                ('is_active', models.BooleanField(default=True)),
                ('text', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.AttendanceRecords')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
                'abstract': False,
            },
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
    ]