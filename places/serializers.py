from rest_framework import serializers

from .models import *

class BasePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'