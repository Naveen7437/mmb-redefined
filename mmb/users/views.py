import copy
import uuid

from datetime import datetime, timedelta
from django.http import Http404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauth2_provider.oauth2_backends import get_oauthlib_core
from oauth2_provider.models import Application
from oauth2_provider.models import RefreshToken, AccessToken
from oauthlib.common import generate_token
from rest_framework_social_oauth2.authentication import SocialAuthentication

from mdata.utils import get_time_diff
from users.app_settings import REFRESH_TIME_IN_MINUTES
from users.utils import create_new_access_token, mail_user_activation_key
from users.models import Profile, User, UserFollower
from users.serializers import UserProfileSerializer, UserSerializer,\
    UserDetailSerializer, UserProfileCreateSerializer, UserAuthDetailsSerializer,\
    UserFollowerSerializer, UserCreateSerializer, PasswordChangeSerializer

expires = datetime.now() + timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])


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
    authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserProfileCreateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user',)
    queryset = Profile.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset:
            raise Http404

        profile_obj = queryset[0]

        # TODO: change to many=True
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = UserProfileSerializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = UserProfileSerializer(profile_obj, context={'request': request})
        return Response(serializer.data)

    def user_thumbnail_details(self, request):
        """
        api to return details of user thumbnail
        """

        response = {}
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

    """
    authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
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




    # def update_profile_pic(self, request, *args, **kwargs):
    #     """
    #     api to update the avatar of user
    #     """
    #     response = copy.deepcopy(self.response)
    #     user = request.user
    #
    #     # TODO: raise error if user is anonymous
    #     if user.is_anonymous():
    #         # response['error'] = "Invalid/Anonymous user"
    #         # return Response(response)
    #         user = get_user_model().objects.get(username="admin")
    #
    #     photo = request.FILES.get('photo')
    #     if photo:
    #         user.avatar = photo
    #         user.save()
    #         response["success"] = True
    #
    #     return Response(response, status=status.HTTP_200_OK)



class UserFollowerViewset(viewsets.ModelViewSet):
    """

    """
    authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserFollowerSerializer
    queryset = UserFollower.objects.all()


class UserCreateViewset(viewsets.ModelViewSet):
    """

    """
    permission_classes = (AllowAny, )
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        """

        """
        data = request.data
        data = dict(data.items())
        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.data)
            user.set_password(data.get('password'))
            user.is_active = False
            user.save()

            # here generating the activation key
            activation_key = str(uuid.uuid4())
            user.activation_key = activation_key
            user.save()

            mail_user_activation_key(user)
            # getting application
            application = Application.objects.get(name="mmb")

            # creating access token
            access_token = AccessToken(
                user=user,
                expires=expires,
                token=generate_token(),
                application=application)

            access_token.save()

            refresh_token = RefreshToken.objects.create(
                user=user,
                token=generate_token(),
                access_token=access_token,
                application=application)

            response = {
                'access_token': access_token.token,
                'token_type': 'Bearer',
                'expires_in': settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'],
                'refresh_token': refresh_token.token
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password
    """

    authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "New password has been updated successfully",
                         "success": True})



def activate_user(request, unique_id):
    """
    activate user and redirect to login page
    """
    # TODO: check expiration of the verification link
    user = get_object_or_404(get_user_model(), activation_key=unique_id)

    if user.is_active == False:
        user.is_active = True

    # TODO: adding redirect url here to login view
    return HttpResponseRedirect("htps://google.com")

