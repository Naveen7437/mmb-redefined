from django.contrib import admin

from .models import Song, SongLike

admin.site.register(Song)
admin.site.register(SongLike)
