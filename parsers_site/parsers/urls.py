from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('flats', FlatsViewSet, basename='flats')


urlpatterns = [
    path('', include(router.urls)),
]
