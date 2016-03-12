from rest_framework import viewsets
from rest_framework.response import Response

from mdata.models import Genre, Instrument
from mdata.serializers import GenreSerializer, InstrumentSerializer


class GenreViewset(viewsets.ModelViewSet):
    """

    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class InstrumentViewset(viewsets.ModelViewSet):
    """

    """
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()