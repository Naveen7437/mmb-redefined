from django.conf.urls import patterns, url, include
from rest_framework import routers
router = routers.SimpleRouter()

from mdata.views import GenreViewset, InstrumentViewset


router = routers.DefaultRouter()
router.register(r'genre', GenreViewset)
router.register(r'instrument', InstrumentViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]