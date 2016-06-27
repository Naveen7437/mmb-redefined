from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from mdata.models import Genre, Instrument
from users.models import Profile, User
from users.serializers import UserProfileSerializer, UserSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()


class UserViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (TokenAuthentication,)
 #   permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


