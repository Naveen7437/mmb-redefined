import copy
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics

from bands.models import Band, BandVacancy, BandMember, BandFollowers,\
    BandVacancyApplication, BandUserInvite
from bands.serializers import BandFollowersSerializer, BandSerializer,\
    BandMemberSerializer, BandVacancySerializer, UserBandMemberSerializer,\
    BandMemberCreateSerializer, BandVacancyApplicationSerializer,\
    BandUserInviteSerializer, BandVacancyFetchSerializer


class BandViewset(viewsets.ModelViewSet):
    """
    Viewset for the band
    """
   #  authentication_classes = (TokenAuthentication,)
   # # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandSerializer
    queryset = Band.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class BandMemberFetch(generics.ListAPIView):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandMemberSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band', 'active')
    queryset = BandMember.objects.all()


class BandMemberCreate(generics.CreateAPIView):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandMemberCreateSerializer


class BandMemberUpdate(generics.UpdateAPIView):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandMemberCreateSerializer
    queryset = BandMember.objects.all()
    #
    # def invite(self, request):
    #     """
    #     invite the member of the band by the email address
    #     """
    #     response = {}
    #     import ipdb;ipdb.set_trace()
    #
    #     data = request.data
    #     email = data.get("email")
    #     band = data.get('band')
    #     user = data.get('user')
    #
    #     if not (email and user and band):
    #         return Response({"error":  "Invalid/Missing fields"})
    #
    #     #TODO: create mail and send to user
    #
    #     return Response({"msg": "mail sent to user successfully",
    #               "success": True})



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
    filter_fields = ('band', 'active')
    queryset = BandVacancy.objects.all()


class BandVacancyFetchViewset(generics.ListAPIView):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandVacancyFetchSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band', 'active')
    queryset = BandVacancy.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class UserBandMemberViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (TokenAuthentication,)
    # #permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserBandMemberSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('member', 'band', 'active')
    queryset = BandMember.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class BandVacancyApplicationViewset(viewsets.ModelViewSet):
    """
    band vacany application apis
    """
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandVacancyApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band_vacancy', 'applicant', 'active')
    queryset = BandVacancyApplication.objects.all()


class BandUserInviteViewset(viewsets.ModelViewSet):
    """
    band user invite apis
    """
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BandUserInviteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('band', 'user', 'active')
    queryset = BandUserInvite.objects.all()

