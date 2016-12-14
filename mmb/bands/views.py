import copy
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bands.models import Band, BandVacancy, BandMember, BandFollowers
from bands.serializers import BandFollowersSerializer, BandSerializer,\
    BandMemberSerializer, BandVacancySerializer


class BandViewset(viewsets.ModelViewSet):
    """

   #  """
   #  authentication_classes = (TokenAuthentication,)
   # # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandSerializer
    queryset = Band.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class BandMemberViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandMemberSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band',)
    queryset = BandMember.objects.all()



class BandFollowersViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandFollowersSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('following_band',)
    queryset = BandFollowers.objects.all()

    def create(self, request, *args, **kwargs):
        response = {}

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        following_band = serializer.data.get('following_band')
        follower = serializer.data.get('follower')

        if not (following_band and follower):
            return Response({'error': 'Invalid request'})

        try:
            BandFollowers.objects.get(following_band__id=following_band, follower__id=follower)
            response['error'] = "object already exists"
        except BandFollowers.DoesNotExist:
            obj = BandFollowers.objects.create(following_band_id=following_band, follower_id=follower)
            response = BandFollowersSerializer(obj).data

        return Response(response)



class BandVacancyViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandVacancySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band',)
    queryset = BandVacancy.objects.all()

