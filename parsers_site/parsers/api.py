# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .serializers import *
from .services import *


class FlatsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Flats.objects.filter(is_archived=False).all()[:15]
    serializer_class = FlatsSerializers
    # pagination_class = StandardResultsSetPagination
    # filter_backends = (DjangoFilterBackend,)

#     filter_fields = [
#         'city',
#         # 'district',
#         # 'micro_district',
#         # 'rooms_quantity'
#     ]
