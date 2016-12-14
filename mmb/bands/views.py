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



class BandVacancyViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandVacancySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band',)
    queryset = BandVacancy.objects.all()

