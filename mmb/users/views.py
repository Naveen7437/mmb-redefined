from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauth2_provider.oauth2_backends import get_oauthlib_core
from rest_framework_social_oauth2.authentication import SocialAuthentication

from mdata.utils import get_time_diff
from users.app_settings import REFRESH_TIME_IN_MINUTES
from users.utils import create_new_access_token
from users.models import Profile, User
from users.serializers import UserProfileSerializer, UserSerializer


class RefreshOauthAuthentication(OAuth2Authentication):
    """
    overriding the oauth2 authentication
    """
    def authenticate(self, request):
        """
        Returns two-tuple of (user, token) if authentication succeeds,
        or None otherwise.
        """
        oauthlib_core = get_oauthlib_core()
        valid, r = oauthlib_core.verify_request(request, scopes=[])

        if r and r.access_token:

            expiry_time = r.access_token.expires

            min_sec = get_time_diff(expiry_time)
            minutes = min_sec[0]

            if minutes < REFRESH_TIME_IN_MINUTES and valid :
                create_new_access_token(r)

        if valid:
            return r.user, r.access_token
        else:
            return None


class UserProfileViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()


class UserViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()






