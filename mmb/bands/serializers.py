from rest_framework import serializers

from bands.models import Band, BandFollowers, BandMember,\
    BandVacancy


class BandSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Band


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
