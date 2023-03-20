from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import *


class FlatsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FlatsSerializers
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Flats.objects.all()[:15]
