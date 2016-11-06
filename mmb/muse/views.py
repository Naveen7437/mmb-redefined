import copy
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_social_oauth2.authentication import SocialAuthentication

from bands.models import Band
from muse.models import Song, SongLike, PlayList, PlayListTrack
from muse.serializers import SongSerializer, SongLikeSerializer,\
    UploadSongForm, PlayListSerializer, PlayListTrackSerializer
from django.contrib.auth import get_user_model
from users.views import RefreshOauthAuthentication


class SongViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SongSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'user')
    # parser_classes = (MultiPartParser, FormParser)
    queryset = Song.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = {}
        user = request.user

        # TODO: to be removed
        if user.is_anonymous():
            user = get_user_model().objects.get(username='admin')

        name = request.POST.get('name')
        tags = request.POST.get('tags')

        # TODO: for now using form as validation only
        form = UploadSongForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                song = Song()
                song.user = user
                song.upload = request.FILES.get('upload')
                song.name = name
                song.tags = tags
                song.save()
                response = SongSerializer(song, context={'request': request}).data
            except:
                response['error'] = "TODO: fuck error(valid)"
        else:
            response['error'] = "TODO: fuck error(invalid)"
        return Response(response)

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


class SongLikeViewset(viewsets.ModelViewSet):
    """

    """
    # authentication_classes = (RefreshOauthAuthentication, SocialAuthentication)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SongLikeSerializer
    queryset = SongLike.objects.all()

    def create(self, request, *args, **kwargs):
        """

        """
        response = {}

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.data.get('user')
        song_id = serializer.data.get('song')

        if not (user_id and song_id):
            return Response({'error': 'Invalid request'})

        try:
            SongLike.objects.get(user__id=user_id, song__id=song_id)
            response['error'] = "object already exists"
        except SongLike.DoesNotExist:
            obj = SongLike.objects.create(user_id=user_id, song_id=song_id)
            response = SongLikeSerializer(obj).data

        return Response(response)


class PlayListViewset(viewsets.ModelViewSet):
    """

    """
    serializer_class = PlayListSerializer
    queryset = PlayList.objects.all()

class PlayListTrackViewset(viewsets.ModelViewSet):
    """

    """
    serializer_class = PlayListTrackSerializer
    queryset = PlayListTrack.objects.all()