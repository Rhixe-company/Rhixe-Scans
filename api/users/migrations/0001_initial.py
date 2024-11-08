# Generated by Django 5.1.1 on 2024-11-03 21:58

import api.users.managers
import api.users.models
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='First Name of User')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Last Name of User')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='User Name')),
                ('images', models.ImageField(blank=True, upload_to=api.users.models.user_image_location, validators=[django.core.validators.FileExtensionValidator(['ico', 'jpg', 'svg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff', 'ttf', 'eot', 'woff', 'woff2'])], verbose_name='Images')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Is superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is staff')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'ordering': ['pk'],
            },
            managers=[
                ('objects', api.users.managers.UserManager()),
            ],
        ),
    ]
