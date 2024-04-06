# Generated by Django 4.2.11 on 2024-03-31 18:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[('1', 'Танки'), ('2', 'Хилы'), ('3', 'Дд'), ('4', 'Торговцы'), ('5', 'Гилдмастеры'), ('6', 'Квестгиверы'), ('7', 'Кузнецы'), ('8', 'Кожевники'), ('9', 'Зельевары'), ('10', 'Мастера Заклинаний')])),
                ('head', models.CharField(max_length=20)),
                ('post_tekst', models.TextField()),
                ('date_create', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, unique=True, upload_to='video_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'avi', 'webm', 'ogv', 'asx'])])),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcore.post')),
            ],
        ),
        migrations.CreateModel(
            name='OneTimeCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, unique=True, upload_to='foto')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcore.post')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, unique=True, upload_to='file_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])])),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcore.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_tekst', models.TextField()),
                ('is_sendet', models.BooleanField(default=False)),
                ('is_ptinjato', models.BooleanField(default=False)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcore.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
