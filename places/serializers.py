from rest_framework import serializers

from .models import *

class BasePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        
    def create(self, validated_data):
        instance = Place.objects.create(**validated_data)
        return instance