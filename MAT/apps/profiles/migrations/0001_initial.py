# Generated by Django 3.0.2 on 2020-01-29 19:05

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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, help_text='This is to make sure deletes are not actual deletes')),
                ('active', models.BooleanField(default=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='Male', max_length=30)),
                ('student_class', models.CharField(default='MC21', max_length=255)),
                ('fullname', models.CharField(default='firstname lastname', max_length=255)),
                ('image', models.URLField(blank=True, default='https://www.google.com/imgres?imgurl=https%3A%2F%2Fmiro', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL)),
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
