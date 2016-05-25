from rest_framework import serializers

from bands.models import Band
from muse.models import SongLike, Song
from muse.utils import check_for_session


class SongSerializer(serializers.ModelSerializer):
    """

    """
    liked = serializers.SerializerMethodField('song_liked_by_user')

    # function to return whether song liked
    # by logged in user or not
    def song_liked_by_user(self, obj):
        request = self.context.get('request')
        user = request.user

        # checking for user/band the session
        is_band, band_id = check_for_session(request)

        # if logged in as band then checking for band
        if is_band and band_id:
            band = Band.objects.get(id=band_id)
            try:
                SongLike.objects.get(band=band, song=obj)
            except SongLike.DoesNotExist:
                return False
            return True
        else:
            try:
                SongLike.objects.get(user__id=user.id, song=obj)
            except SongLike.DoesNotExist:
                return False
            return True

    class Meta:
        model = Song
        fields = ('id', 'user', 'band', 'name', 'likes',
                  'upload', 'duration', 'liked')


class SongLikeSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = SongLike
