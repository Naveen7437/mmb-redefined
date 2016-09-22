from django.conf.urls import patterns, url, include
from rest_framework import routers

from muse.views import SongViewset, SongLikeViewset

router = routers.DefaultRouter()
router.register(r'^song', SongViewset)
router.register(r'song-like', SongLikeViewset)

urlpatterns = [
    url(r'', include(router.urls)),
]