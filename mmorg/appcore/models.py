from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import os
from django.conf import settings
from django import forms
from django.utils import timezone



class Post(models.Model):
    class CategoryType(models.TextChoices):
        CAT1 = '1', 'Танки'
        CAT2 = '2', 'Хилы'
        CAT3 = '3', 'ДД'
        CAT4 = '4', 'Торговцы'
        CAT5 = '5', 'Гилдмастеры'
        CAT6 = '6', 'Квестгиверы'
        CAT7 = '7', 'Кузнецы'
        CAT8 = '8', 'Кожевники'
        CAT9 = '9', 'Зельевары'
        CAT10 = '10', 'Мастера_заклинаний'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CategoryType.choices, null=False)
    head = models.CharField(max_length=20)
    post_tekst = models.TextField()
    date_create = models.DateTimeField(default=timezone.now)
    foto = models.ManyToManyField('Foto', through='PostFoto')
    video = models.ManyToManyField('Video', through='PostVideo')
    file = models.ManyToManyField('File', through='PostFile')

    def get_author(self):
        author = self.user
        return author

    def get_absolute_url(self):
        x = 'posts_detail'
        return reverse(x, args=[str(self.id)])

    def __str__(self):
        return f'{self.head}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='Postes', on_delete=models.CASCADE)
    comment_tekst = models.TextField()
    is_sendet = models.BooleanField(null=False, default=False)
    is_ptinjato = models.BooleanField(null=False, default=False)
    date_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        x = 'posts_detail'
        return reverse(x, args=[str(self.post_id)])

    def __str__(self):
        return f'{self.comment_tekst[:20]}'

class Foto(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)
    image = models.ImageField(upload_to='foto', blank=True, unique=True)
    date_create = models.DateTimeField(auto_now_add=True)

    @property
    def photo_url(self):
        return format_html('<img src="{}" width="100" height="100" alt="">'.format(self.image.url))

    def __str__(self):
        return format_html('<img src="{}" width="100" height="100" alt="">'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('fotos')


class Video(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video_uploaded', null=True, blank=True, unique=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'avi', 'webm', 'ogv', 'asx'])])
    date_create = models.DateTimeField(auto_now_add=True)

    @property
    def video_url(self):
        return format_html("""
                <video width = "100" height = "100" controls = "controls" poster = "video/duel.jpg">
                <source src = {}>
                video не поддерживается вашим браузером.
                </video>
                """.format(self.video.url))

    def __str__(self):
        return format_html("""
        <video width = "100" height = "100" controls = "controls" poster = "video/duel.jpg">
        <source src = {}>
        video не поддерживается вашим браузером.
        </video>
        """.format(self.video.url))

    def get_absolute_url(self):
        return reverse('video_edit')


class File(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file_uploaded', null=True, blank=True, unique=True,
                             validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    date_create = models.DateTimeField(auto_now_add=True)

    def read_txt(self):
        name, extension = os.path.splitext(self.file.name)
        if 'txt' in extension:
            path = os.sep.join([settings.MEDIA_ROOT, self.file.name])
            with open(path, 'r') as f:
                lines = f.readlines()
                return lines

    def __str__(self):
        tekst = self.read_txt()
        return tekst[0][:10]


class OneTimeCode(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.code

class PostFoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE)

class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)


