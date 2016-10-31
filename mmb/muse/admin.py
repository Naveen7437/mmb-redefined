from django.contrib import admin

from .models import Song, SongLike, PlayListTrack, PlayList

admin.site.register(Song)
admin.site.register(SongLike)
admin.site.register(PlayListTrack)
admin.site.register(PlayList)
