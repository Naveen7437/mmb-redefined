from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from mdata.models import Genre, Instrument
from mmb.settings import AUTH_USER_MODEL
from .app_settings import CITIES, YEAR_CHOICES, MEMBER_TYPE, SONG_TAGS


def get_upload_file_name(instance, filename):
    return 'audio/{0}_{1}/{2}'.format(slugify(instance.user_id), instance.user.username, filename)


class Band(models.Model):
    name = models.CharField(unique=True, max_length=255)
    genre = models.ManyToManyField(Genre)
    member = models.ManyToManyField(AUTH_USER_MODEL, through='BandMember')
    # vacancy = models.ManyToManyField(Instrument)
    location = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)
    follower_count = models.IntegerField(default=0)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.now().year)
    desc = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='band_admin')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)


class BandMember(models.Model):
    band = models.ForeignKey(Band)
    member = models.ForeignKey(AUTH_USER_MODEL)
    instrument = models.ForeignKey(Instrument)
    type = models.CharField(max_length=9, choices=MEMBER_TYPE, default='Permanent')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.band, self.member)


class BandVacancy(models.Model):
    band = models.ForeignKey(Band)
    instrument = models.ForeignKey(Instrument)
    type = models.CharField(max_length=9, choices=MEMBER_TYPE, default='Permanent')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Band vacancies'

    def __str__(self):
        return '{} - {}'.format(self.band, self.instrument)


class BandVacancyApplication(models.Model):
    band_vacancy = models.ForeignKey(BandVacancy)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='applicant')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.band_vacancy.band.name, self.user.username)


class BandFollowers(models.Model):
    follower = models.ForeignKey(AUTH_USER_MODEL, related_name='band_follower')
    following_band = models.ForeignKey(Band, related_name='band_following')

    def __str__(self):
        return '{} - {}'.format(self.follower.username, self.following.name)
