from rest_framework import serializers
from .models import *


class FlatsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flats
        fields = '__all__'
