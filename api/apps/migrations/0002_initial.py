# Generated by Django 5.1.1 on 2024-11-03 21:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apps', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comicuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapterimagesitem',
            name='comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.comic'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comicchapters', to='apps.comic'),
        ),
        migrations.AddField(
            model_name='comicimagesitem',
            name='comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comicitems', to='apps.comic'),
        ),
        migrations.AddField(
            model_name='comicimagesitem',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.comicimage'),
        ),
        migrations.AddField(
            model_name='comic',
            name='images',
            field=models.ManyToManyField(through='apps.ComicImagesItem', to='apps.comicimage'),
        ),
        migrations.AddField(
            model_name='comment',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chaptercomments', to='apps.chapter'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comic',
            name='genres',
            field=models.ManyToManyField(blank=True, to='apps.genre'),
        ),
        migrations.AddField(
            model_name='comic',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comictype', to='apps.type'),
        ),
        migrations.AddField(
            model_name='usersitem',
            name='comic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='apps.comic'),
        ),
        migrations.AddField(
            model_name='usersitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comic',
            name='users',
            field=models.ManyToManyField(blank=True, through='apps.UsersItem', to=settings.AUTH_USER_MODEL),
        ),
    ]
