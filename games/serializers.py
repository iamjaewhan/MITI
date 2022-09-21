from django.utils import timezone
from rest_framework import serializers

from .models import *
from users.serializers import BaseUserSerializer
from places.serializers import BasePlaceSerializer

class BaseGameSerializer(serializers.ModelSerializer):
    place = BasePlaceSerializer(read_only=True)
class GameRegisterSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    
    class Meta:
        model = Game
        fields = '__all__'
        
    def validate_start_datetime(self, value):
        if value > timezone.now():
            return value
        raise ValueError()
    
    def validate_end_datetime(self, value):
        if value > timezone.now():
            return value
        raise ValueError()
    
    def validate(self, data):
        if data['start_datetime'] >= data['end_datetime']:
            raise ValueError()
        return data
    
    
class GameDetailSerializer(serializers.ModelSerializer):
    host = BaseUserSerializer(read_only=True)
    
    class Meta:
        model = Game
        fields = '__all__'
        
        
class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'
        
    def validate(self, data):
        game = data['game']
        if game.invitation > len(Participation.objects.filter(game=game.id)):
            return data