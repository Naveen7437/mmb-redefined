from django.contrib.auth import get_user_model
from rest_framework import serializers


from bands.models import Band, BandFollowers, BandMember,\
    BandVacancy


class BandSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Band

    def create(self, validated_data):
        # TODO: need rework
        obj = Band()
        obj.lable  = validated_data.get('label')
        obj.location  = validated_data.get('location')
        obj.year  = validated_data.get('year')
        obj.name  = validated_data.get('name')
        obj.desc  = validated_data.get('desc')
        # obj.genre = validated_data.get('genre')
        user = self.context.get('request').user
        if user.is_anonymous():
            obj.created_by = get_user_model().objects.get(username="admin")
        else:
            obj.created_by = user

        obj.save()
        for genre in validated_data.get('genre'):
            obj.genre.add(genre)

        return obj


class BandVacancySerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandVacancy


class BandFollowersSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandFollowers


class BandMemberSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = BandMember
