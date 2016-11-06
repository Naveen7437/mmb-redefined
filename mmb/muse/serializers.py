import os
from django import forms
from django.core.exceptions import ValidationError
from rest_framework import serializers

from bands.models import Band
from muse.models import SongLike, Song, PlayListTrack, PlayList
from muse.utils import check_for_session


class SongSerializer(serializers.ModelSerializer):
    """

    """
    song_like_id = serializers.SerializerMethodField('song_liked_by_user')
    full_name = serializers.CharField(source='user.get_full_name',
                                      required=False, read_only=True)
    username = serializers.CharField(source='user.username', required=False,
                                     read_only=True)

    def song_liked_by_user(self, obj):
        """
        function to return whether song liked
        by logged in user or not
        """

        request = self.context.get('request')
        user = request.user

        # checking for user/band the session
        is_band, band_id = check_for_session(request)

        # if logged in as band then checking for band
        if is_band and band_id:
            band = Band.objects.get(id=band_id)
            try:
                song_like = SongLike.objects.get(band=band, song=obj)
            except SongLike.DoesNotExist:
                return None
            return song_like.id
        else:
            try:
                song_like = SongLike.objects.get(user__id=user.id, song=obj)
            except SongLike.DoesNotExist:
                return None
            return song_like.id

    class Meta:
        model = Song
        # fields = ('id', 'user', 'band', 'name', 'likes',
        #           'upload', 'duration', 'liked', 'tags', 'rating', 'full_name')


class SongLikeSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = SongLike


class UploadSongForm(forms.Form):
    """
    form to validate the upload file
    """
    upload = forms.FileField()

    def clean_upload(self):
        cleaned_data = super(UploadSongForm, self).clean()
        file = cleaned_data.get('upload', False)
        if file:
            if file._size > 15*1024*1024:
                raise ValidationError("Audio file too large ( > 15mb )")
            if not file.content_type in ["audio/mpeg","video/mp4","audio/mp3"]:
                raise ValidationError("Content-Type is not mpeg")
            if not os.path.splitext(file.name)[-1] in [".mp3",".wav",".mp4"]:
                raise ValidationError("Doesn't have proper extension")
             # Here we need to now to read the file and see if it's actually
             # a valid audio file. I don't know what the best library is to
             # to do this
            # if not some_lib.is_audio(file.content):
            #     raise ValidationError("Not a valid audio file")
            return file
        else:
            raise ValidationError("Couldn't read uploaded file")


class PlayListTrackSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = PlayListTrack


class PlayListSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = PlayList