from django.contrib import admin
from .models import Post, Comment, Foto, Video, File
from django.utils.html import format_html


@admin.register(Foto)
class Foto(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" alt="obj.image.id"/>'.format(obj.image.url))
    image_tag.short_description = 'Image'
    list_display = ['image_tag',]

admin.site.register(Post)
admin.site.register(Comment)
#admin.site.register(Foto)
admin.site.register(Video)
admin.site.register(File)

