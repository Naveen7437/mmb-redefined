from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,\
                        BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from mdata.models import Genre, Instrument
from mdata.serializers import GenreSerializer, InstrumentSerializer



class GenreViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class InstrumentViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()

    # def create(self, *args, **kwargs):
    #     data = {"instrument": "Piano",
    #             "instrumentalist":"dsdsd"}
    #     s = InstrumentSerializer(data=data)
    #     if s.is_valid():
    #         s.save()
    #     return Response(s.data)