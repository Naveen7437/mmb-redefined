# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from unidecode import unidecode
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from mdata.models import Genre, Instrument
from .app_settings import CITIES, PHONE_REG, USER_TYPE


def get_upload_file_name(instance, filename):
    """
    function to set path for uploading images
    """
    if not isinstance(filename, str):
        map(filename, str)

    filename = unidecode(smart_text(filename))

    # if instance.band:
    #     id = instance.band.id
    #     name = 'band'
    # else:
    id = instance.id
    name = 'user'

    return 'images/{0}/{1}'.format(name, id)


class User(AbstractUser):
    """
    User class: adding fields to the user table
    """
    name = models.CharField(blank=True, max_length=255)
    type = models.CharField(max_length=10, choices=USER_TYPE, default='Listener')
    avatar = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

#
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    instrument = models.ManyToManyField(Instrument, blank=True, null=True)
    # todo - need list of all colleges if possible
    college = models.CharField(max_length=100, blank=True, null=True)
    current_city = models.CharField(choices=CITIES, max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    following_count = models.IntegerField(default=0)
    followed_by_count = models.IntegerField(default=0)
    band_follow_count = models.IntegerField(default=0)
    join_band = models.BooleanField(default=False)
    with_band = models.BooleanField(default=False)
    create_band = models.BooleanField(default=False)

    about_me = models.CharField(max_length=255, blank=True, null=True)
    # other_link = models.CharField(max_length=255, blank=True, null=True)    #This is the link which user updates

    def __str__(self):
        return str(self.user)

    def update(self,*args,**kwargs):
        self.college = kwargs.get('college')
        self.current_city = kwargs.get('current_city')
        self.phone = kwargs.get('phone')
        self.website = kwargs.get('website')
        self.about_me = kwargs.get('about_me')
        self.save()


class UserFollower(models.Model):
    """

    """
    # one who follows
    follower = models.ForeignKey(User, related_name='follower')

    # one who is being followed
    following = models.ForeignKey(User, related_name='following')
    # following_is_user = models.BooleanField()

    def __str__(self):
        return '{} - {}'.format(self.follower.username, self.following.name)
