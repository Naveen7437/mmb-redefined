from rest_framework import serializers
from muse.models import SongLike, Song


class SongSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Song


class SongLikeSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = SongLike
