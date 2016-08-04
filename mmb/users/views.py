from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework_social_oauth2.authentication import SocialAuthentication

from mdata.models import Genre, Instrument
from users.models import Profile, User
from users.serializers import UserProfileSerializer, UserSerializer


class UserProfileViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (OAuth2Authentication, SocialAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()


class UserViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (OAuth2Authentication, SocialAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


