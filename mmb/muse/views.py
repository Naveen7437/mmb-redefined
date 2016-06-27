import copy
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from bands.models import Band
from muse.models import Song, SongLike
from muse.serializers import SongSerializer, SongLikeSerializer


class SongViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
   # permission_classes = (IsAuthenticated,)
    serializer_class = SongSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'user')
    queryset = Song.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned songs
        against a `count` query parameter in the URL.
        """
        queryset = Song.objects.all()
        count = self.request.query_params.get('count', None)
        if count:
            try:
                count = int(count)
                queryset = queryset.order_by('-id')[:count]
            except:
                pass
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}




class SongLikeViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    serializer_class = SongLikeSerializer
    queryset = SongLike.objects.all()
