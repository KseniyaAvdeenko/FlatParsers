# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from .serializers import *
from .services import *


class FlatsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = FlatsSerializers

    # pagination_class = StandardResultsSetPagination
    # filter_backends = (DjangoFilterBackend,)
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Flats.objects.filter(is_archived=False).all()
        return Flats.objects.filter(pk=pk)
