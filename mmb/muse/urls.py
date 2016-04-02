from django.conf.urls import patterns, url, include
from rest_framework import routers
router = routers.SimpleRouter()

from muse.views import SongViewset



router = routers.DefaultRouter()
router.register(r'song', SongViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]