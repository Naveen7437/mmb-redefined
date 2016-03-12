from rest_framework import serializers

from mdata.models import Genre, Instrument


class GenreSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Genre


class InstrumentSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Instrument