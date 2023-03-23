from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from .api import *


router = SimpleRouter()
router.register('flats', FlatsViewSet, basename='flats')

urlpatterns = [
    path('', include(router.urls)),
]







# urlpatterns = [
#     path('', views.flats_search, name='search'),
# ]










# path('', FlatsViewSet.as_view({'get': 'list'}))
# path('', FlatsListView.as_view())