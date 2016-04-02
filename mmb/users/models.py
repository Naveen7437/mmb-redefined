# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from mdata.models import Genre, Instrument
from .app_settings import CITIES, PHONE_REG, USER_TYPE


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    type = models.CharField(max_length=10, choices=USER_TYPE, default='Listener')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    user = models.ForeignKey(User)
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
    follower = models.ForeignKey(User, related_name='follower')
    # follower_is_user = models.BooleanField()
    following = models.ForeignKey(User, related_name='following')
    # following_is_user = models.BooleanField()

    def __str__(self):
        return '{} - {}'.format(self.follower.username, self.following.name)
