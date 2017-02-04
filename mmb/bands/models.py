from unidecode import unidecode
from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_text

from mdata.models import Genre, Instrument
from mmb.settings import AUTH_USER_MODEL
from .app_settings import YEAR_CHOICES, MEMBER_TYPE, ACCESS_CHOICES, VACANCY_CHOICES, ACTIVE_CHOICES


def get_upload_file_name(instance, filename):
    """
    function to set path for uploading images
    """
    return 'images/band/{0}'.format(instance.id)


class Band(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to=get_upload_file_name,
                              default="images/band/image/default.jpeg", blank=True)
    cover = models.ImageField(upload_to=get_upload_file_name,
                              default="images/band/cover/default.jpeg", blank=True)

    member = models.ManyToManyField(AUTH_USER_MODEL, through='BandMember',
                                    through_fields=('band', 'member'))

    location = models.CharField(max_length=125, blank=True, null=True)
    label = models.CharField(max_length=125, blank=True, null=True)
    follower_count = models.IntegerField(default=0)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES,
                               default=datetime.now().year)
    desc = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='band_admin', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    fb_link = models.CharField(max_length=255, blank=True, null=True)
    twitter_link = models.CharField(max_length=255, blank=True, null=True)
    google_link = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class BandMember(models.Model):
    band = models.ForeignKey(Band)
    member = models.ForeignKey(AUTH_USER_MODEL, related_name="band_member")
    added_by = models.ForeignKey(AUTH_USER_MODEL, related_name='added_by')
    instrument = models.ForeignKey(Instrument)
    active = models.BooleanField(default=True)
    access = models.CharField(max_length=25, choices=ACCESS_CHOICES, default="basic", blank=True)
    type = models.CharField(max_length=9, choices=MEMBER_TYPE, default='Permanent')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return '{} - {}'.format(self.band, self.member)


class BandVacancy(models.Model):
    band = models.ForeignKey(Band)
    instrument = models.ForeignKey(Instrument)
    added_by = models.ForeignKey(AUTH_USER_MODEL, blank=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=9, choices=MEMBER_TYPE, default='Permanent')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Band vacancies'

    def __str__(self):
        return '{} - {}'.format(self.band, self.instrument)


class BandVacancyApplication(models.Model):
    band_vacancy = models.ForeignKey(BandVacancy)
    applicant = models.ForeignKey(AUTH_USER_MODEL, related_name='applicant')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return '{} - {}'.format(self.band_vacancy.band.name, self.user.username)


class BandFollowers(models.Model):
    # user following band
    follower = models.ForeignKey(AUTH_USER_MODEL, related_name='band_follower')
    # band to be followed
    following_band = models.ForeignKey(Band, related_name='band_following')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{} - {}'.format(self.follower.username, self.following_band.name)


# class BandUserInvite(models.Model):
#     band = models.ForeignKey(Band)
#     user = models.ForeignKey(AUTH_USER_MODEL, related_name="band_member")
#     invited_by = models.ForeignKey(AUTH_USER_MODEL, related_name='added_by', blank=True)


