# Generated by Django 3.0.8 on 2021-10-05 08:47

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('is_professional', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone_num', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='profile_img')),
                ('info', models.TextField(blank=True, max_length=150)),
                ('website', models.TextField(blank=True, max_length=150)),
                ('profile_name', models.CharField(blank=True, max_length=50)),
                ('gender', models.CharField(blank=True, max_length=15)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='api.User')),
            ],
        ),
    ]
