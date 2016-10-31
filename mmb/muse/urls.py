from django.conf.urls import patterns, url, include
from rest_framework import routers

from muse.views import SongViewset, SongLikeViewset, PlayListViewset,\
    PlayListTrackViewset

router = routers.DefaultRouter()
router.register(r'^song', SongViewset)
router.register(r'song-like', SongLikeViewset)
router.register(r'^playlist', PlayListViewset)
router.register(r'^tracks', PlayListTrackViewset)

urlpatterns = [
    url(r'', include(router.urls)),
]