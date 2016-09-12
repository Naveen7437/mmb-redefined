import copy
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, filters
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
from users.serializers import UserProfileSerializer, UserSerializer,\
    UserDetailSerializer, UserProfileCreateSerializer, UserAuthDetailsSerializer


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
    user profile viewset
    """
    # authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileCreateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user',)
    queryset = Profile.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserProfileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def user_thumbnail_details(self, request):
        """
        api to return details of user thumbnail
        """

        response = copy.deepcopy(self.response)
        ids = request.query_params.get('ids', None)
        count = request.query_params.get('count', None)

        if not ids and not count:
            response['detail'] = "Invalid Query parameters"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # getting list of user #id
        user_ids = ids.split(',') if ids else None

        if user_ids:
            try:
                user_ids = list(map(int, user_ids))
            except ValueError:
                response['detail'] = "Invalid User ids"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user_profile_queryset = Profile.objects.filter(user__id__in=user_ids)

            serializer = UserDetailSerializer(user_profile_queryset,
                                              context={'request': request}, many=True)

            # if serializer.is_valid():
            return Response(serializer.data)

        try:
            count = int(count)
        except ValueError:
            response['detail'] = "Invalid value of count"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset.order_by('-id')[:count]

        serializer = UserDetailSerializer(queryset, many=True,
                                          context={'request': request})
        return Response(serializer.data)


class UserViewset(viewsets.ModelViewSet):
    """

    # """
    # authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    response = {
        "data": {},
        "error": "",
        "success": False
    }

    def validate_username(self, request, *args, **kwargs):
        """
        check if the username still exists or not
        :param request: username
        :return: True if username
        doesn't exist in system
        """
        response = copy.deepcopy(self.response)
        username = kwargs.get('username')

        if not username:
            response['error'] = "Invalid Query parametrs"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            get_user_model().objects.get(username=username)
            if request.user.username == username:
                response['success'] = True
            else:
                response['error'] = "Username already exists"
        except User.DoesNotExist:
            response['success'] = True

        return Response(response, status=status.HTTP_200_OK)

    def auth_details(self, request, *args, **kwargs):
        """
        return basic user details
        :param request:
        :return:
        """
        response = copy.deepcopy(self.response)
        user = request.user

        if user.is_anonymous():
            response['error'] = "Invalid/Anonymous user"
            return Response(response)

        serializer = UserAuthDetailsSerializer(user, context={'request': request})
        response['data'] = serializer.data
        response['success'] = True
        return Response(response, status=status.HTTP_200_OK)








