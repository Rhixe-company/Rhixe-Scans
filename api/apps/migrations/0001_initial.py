# Generated by Django 5.1.1 on 2024-11-03 21:58

import api.apps.models
import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Artist',
                'verbose_name_plural': 'Artists',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Uuid')),
                ('name', models.CharField(max_length=500, verbose_name='Name')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=500, unique=True, verbose_name='Slug')),
                ('spider', models.CharField(max_length=500, verbose_name='Spider')),
                ('url', models.URLField(max_length=500, verbose_name='Url')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(blank=True)),
                ('numPages', models.PositiveSmallIntegerField(verbose_name='Total Pages')),
            ],
            options={
                'verbose_name': 'Chapter',
                'verbose_name_plural': 'Chapters',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ChapterImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500, unique=True, verbose_name='Url')),
                ('checksum', models.CharField(blank=True, max_length=500, verbose_name='Checksum')),
                ('status', models.CharField(choices=[('uptodate', 'Uptodate'), ('downloaded', 'Downloaded')], default='downloaded', max_length=11, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='ComicImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500, unique=True, verbose_name='Url')),
                ('checksum', models.CharField(blank=True, max_length=500, verbose_name='Checksum')),
                ('status', models.CharField(choices=[('uptodate', 'Uptodate'), ('downloaded', 'Downloaded')], default='downloaded', max_length=11, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='ComicImagesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=500, upload_to=api.apps.models.comic_location, validators=[django.core.validators.FileExtensionValidator(['ico', 'jpg', 'svg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff', 'ttf', 'eot', 'woff', 'woff2'])], verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Body')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Manga', 'Manga'), ('Manhwa', 'Manhwa'), ('Manhua', 'Manhua')], max_length=6, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.CreateModel(
            name='UsersItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Usersitem',
                'verbose_name_plural': 'UsersItems',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ChapterImagesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=500, upload_to=api.apps.models.panel_location, validators=[django.core.validators.FileExtensionValidator(['ico', 'jpg', 'svg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff', 'ttf', 'eot', 'woff', 'woff2'])], verbose_name='Image')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapteritems', to='apps.chapter')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.chapterimage')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='images',
            field=models.ManyToManyField(through='apps.ChapterImagesItem', to='apps.chapterimage'),
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Uuid')),
                ('title', models.CharField(max_length=500, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=500, unique=True, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Ongoing', 'Ongoing'), ('Hiatus', 'Hiatus'), ('Dropped', 'Dropped'), ('Season End', 'Season End'), ('Coming Soon', 'Coming Soon')], max_length=15, verbose_name='Status')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Rating')),
                ('serialization', models.CharField(blank=True, max_length=500, verbose_name='Serialization')),
                ('numChapters', models.PositiveIntegerField(verbose_name='Total Chapters')),
                ('spider', models.CharField(max_length=500, verbose_name='Spider')),
                ('url', models.URLField(max_length=500, verbose_name='Url')),
                ('numItems', models.PositiveSmallIntegerField(verbose_name='Total Items')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(blank=True)),
                ('artist', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comicartist', to='apps.artist')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='comicauthor', to='apps.author')),
            ],
            options={
                'verbose_name': 'Comic',
                'verbose_name_plural': 'Comics',
                'ordering': ['-updated_at'],
            },
        ),
    ]
