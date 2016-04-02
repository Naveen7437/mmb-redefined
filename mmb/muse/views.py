from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from muse.models import Song, SongLike
from muse.serializers import SongSerializer, SongLikeSerializer


class SongViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = SongSerializer
    queryset = Song.objects.all()


class SongLikeViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = SongLikeSerializer
    queryset = SongLike.objects.all()