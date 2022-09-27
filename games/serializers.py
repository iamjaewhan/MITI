from django.utils import timezone
from rest_framework import serializers

from .models import *
from users.serializers import BaseUserSerializer
from places.serializers import BasePlaceSerializer

class BaseGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        

class GameRegisterSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    
    class Meta:
        model = Game
        fields = '__all__'
        
    def validate_start_datetime(self, value):
        """_summary_
        start_datetime 유효성 점검

        Raises:
            ValueError: 현재 시간보다 앞서는 시간일 경우
        """
        if value > timezone.now():
            return value
        raise ValueError()
    
    def validate_end_datetime(self, value):
        """_summary_
        end_datetime 유효성 점검

        Raises:
            ValueError: 현재 시간보다 앞서는 시간일 경우
        """
        if value > timezone.now():
            return value
        raise ValueError()
    
    def validate(self, data):
        """_summary_
        start_datetime, end_datetime 관계 유효성 점검

        Raises:
            ValueError: 종료시간이 시작 시간보다 앞서는 경우
        """
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
        """_summary_
        Participation 데이터 생성 가능성 점검
        
        Raises:
            403 : 초대가 완료되어 지원이 불가능한 경우
        """
        game = data['game']
        if game.invitation > len(Participation.objects.filter(game=game.id)):
            return data
                
    def delete(self):
        """_summary_
        serializer로 전달한 객체를 삭제
        """
        self.instance.delete()
        