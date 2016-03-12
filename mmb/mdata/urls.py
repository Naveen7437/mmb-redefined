from django.conf.urls import patterns, url, include
from rest_framework import routers
router = routers.SimpleRouter()

from mdata.views import GenreViewset, InstrumentViewset

# router = DefaultRouter()
# router.register(r'users', UserProfile)
urlpatterns = [
    url(r'^get/$', GenreViewset.as_view({'get':'list'})),
    url(r'^ins/$', InstrumentViewset.as_view({'get':'list'})),
]
urlpatterns += router.urls