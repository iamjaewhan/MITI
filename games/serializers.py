from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from .models import *
from users.serializers import BaseUserSerializer
from places.serializers import BasePlaceSerializer
from alarms.models import Alarm
from utils.validators import GameTimeValidator
from constants.custom_exceptions import (
    DuplicatedParticipationException,
    UnParticipatableException,
    FullGameException
)

class BaseGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        

class GameRegisterSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(validators=[GameTimeValidator()])
    end_datetime = serializers.DateTimeField(validators=[GameTimeValidator()])
    
    class Meta:
        model = Game
        fields = '__all__'
        
    
    def validate(self, data):
        """_summary_
        start_datetime, end_datetime 관계 유효성 점검

        Raises:
            ValueError: 종료시간이 시작 시간보다 앞서는 경우
        """
        if data['start_datetime'] >= data['end_datetime']:
            raise ValidationError("유효한 경기 시간이 아닙니다.")
        return data
        
        
class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'
        
    def validate(self, data):
        """_summary_
        Participation 데이터 생성 가능성 점검
        
        Raises:
            400 : 모집이 완료된 경기인 경우
        """
        game = data['game']
        if game.invitation > game.player:
            return data
        raise FullGameException()
    def delete(self):
        """_summary_
        serializer로 전달한 객체를 삭제
        """
        self.instance.delete()
        