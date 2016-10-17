# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO, StringIO

from PIL import Image
from resizeimage import resizeimage

from unidecode import unidecode
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.db import models
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.db.models.signals import pre_save
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
    activation_key = models.CharField(max_length=127, blank=True)
    avatar = models.ImageField(upload_to=get_upload_file_name,
                               default="images/user/default.jpeg", blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def save(self, *args, **kwargs):

        image_name = os.path.split(self.avatar.name)[-1]

        # TODO: change this ***** and move to task
        if image_name != "default.jpeg":
            pil_image_obj = Image.open(self.avatar)
            new_image = resizeimage.resize_thumbnail(pil_image_obj, (300, 450))

            new_image_io = BytesIO()
            new_image.save(new_image_io, format='JPEG')

            temp_name = self.avatar.name
            self.avatar.delete(save=False)

            self.avatar.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

        super(User, self).save(*args, **kwargs)

# @receiver(pre_save, sender=User)
# def set_image_size(sender, instance=None, created=False, **kwargs):
#     """
#     set size before uploading image
#     """
#     if instance:
#         im = get_thumbnail(instance.avatar, '300x450', crop='center', quality=99)
        #
        #
        # image_name = os.path.split(instance.avatar.name)[-1]
        #
        # # don't need to save default image everytime so checking
        # # if image is default type then bypassing this method
        #
        # if image_name == "default.png":
        #
        #     # open image using PIL
        #     img = Image.open(instance.avatar.path)
        #     img.resize((300, 450), PIL.Image.ANTIALIAS)
        #
        #     temp_handle = BytesIO()
        #     img.save(temp_handle, 'png')
        #     temp_handle.seek(0)
        #
        #     img_file = SimpleUploadedFile(image_name, temp_handle.read(),
        #                                   content_type='image/png')
        #
        #     instance.avatar.save('{0}.png'.format(os.path.splitext(img_file.name)[0]), img_file, save=False)


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    genre = models.ManyToManyField(Genre, blank=True, null=True)
    instrument = models.ManyToManyField(Instrument, blank=True, null=True)
    # TODO: - need list of all colleges if possible
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
    fb_link = models.CharField(max_length=255, blank=True, null=True)    # This is the facebook link which user updates
    twitter_link = models.CharField(max_length=255, blank=True, null=True)  # This is the link which user updates
    google_link = models.CharField(max_length=255, blank=True, null=True)   # This is the link which user updates

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

