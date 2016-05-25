from django.db import models
from urllib.request import urlretrieve
import audioread

from bands.models import Band
from mmb.settings import AUTH_USER_MODEL
from .app_settings import SONG_TAGS


def get_upload_file_name(instance, filename):
    if instance.band:
        id = instance.band.id
        name = instance.band.name
    else:
        id = instance.user.id
        name = instance.user.username
    return 'audio/{0}_{1}/{2}'.format(id, name, filename)


class Song(models.Model):
    # type = models.CharField(choices=SONG_TYPES, default='Audio')
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, default=None)
    band = models.ForeignKey(Band, null=True, blank=True, default=None)
    name = models.CharField(max_length=255)
    tags = models.CharField(choices=SONG_TAGS, max_length=255)
    likes = models.IntegerField(default=0)
    rating = models.IntegerField(default=3)
    upload = models.FileField(upload_to=get_upload_file_name)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    duration = models.FloatField(default=0.0)
    # singer = models.CharField(blank=True, max_length=255)
    # label = models.CharField(blank=True, max_length=255)


    def __str__(self):
        return '{}'.format(self.name)

    # def save(self, *args, **kwargs):
    #     audio = audioread.audio_open(self.upload.url)
    #     self.duration = audio.duration
    #     super(Song, self).save(*args, **kwargs)





class SongLike(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, default=None)
    band = models.ForeignKey(Band, null=True, blank=True, default=None)
    song = models.ForeignKey(Song)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.song.name)