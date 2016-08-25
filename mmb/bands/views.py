import copy
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from bands.models import Band, BandVacancy, BandMember, BandFollowers
from bands.serializers import BandFollowersSerializer, BandSerializer,\
    BandMemberSerializer, BandVacancySerializer


class BandViewset(viewsets.ModelViewSet):
    """

   #  """
   #  authentication_classes = (TokenAuthentication,)
   # # permission_classes = (IsAuthenticated,)
    serializer_class = BandSerializer
    queryset = Band.objects.all()


class BandMemberViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticated,)
    serializer_class = BandMemberSerializer
    queryset = BandMember.objects.all()


class BandFollowersViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticated,)
    serializer_class = BandFollowersSerializer
    queryset = BandFollowers.objects.all()


class BandVacancyViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticated,)
    serializer_class = BandVacancySerializer
    queryset = BandVacancy.objects.all()
