from rest_framework import serializers

from .models import *
from places.serializers import BasePlaceSerializer

class BaseGameSerializer(serializers.ModelSerializer):
    place = BasePlaceSerializer(read_only=True)
    
    class Meta:
        model = Game
        fields = '__all__'