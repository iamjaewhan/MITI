from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
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
        
    def create(self, validated_data):
        """_summary_
        경기 참여 기록을 생성

        Raises:
            DuplicatedParticipationException: 참여 기록이 이미 존재하는 경우

        Returns:
            Participation 객체: 생성된 참여 객체
        """
        try:
            with transaction.atomic():
                obj, created = self.Meta.model.objects.get_or_create(**validated_data)
                if created:
                    return obj
                if obj.deleted_at:
                    return obj
                raise DuplicatedParticipationException()
        except IntegrityError :
            raise DuplicatedParticipationException()

    def delete(self):
        """_summary_
        serializer로 전달한 객체를 삭제
        """
        self.instance.delete()
    

class PaymentRedirectUrlSerializer(serializers.Serializer):
    next_redirect_pc_url = serializers.CharField()
    next_redirect_app_url = serializers.CharField()
    next_redirect_mobile_url = serializers.CharField()
    
    
    
from payment.models import ParticipationPaymentRequest

class ParticipationPaymentRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParticipationPaymentRequest
        fields = '__all__'
        
    def get_or_create(self):
        participation_queryset = self.Meta.model.objects.filter(
            participation=self.initial_data['participation'])
        
        if participation_queryset.exists():
            participation_obj = participation_queryset.first()
            participation_obj.save()
            self.instance = participation_obj
            return participation_obj
        
        if self.is_valid(raise_exception=True):
            participation_obj = self.save()
            self.instance = participation_obj
            return participation_obj

    def set_tid(self, tid):
        self.instance.tid = tid
        self.instance.save(update_fields=['tid'])
                
            
            
        