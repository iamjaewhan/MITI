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
    
    
    
    
from payment.models import *
        


class PaymentResultSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(required=False)
    
    class Meta:
        model = PaymentResult
        fields = (
            'aid',
            'item_name',
            'quantity',
            'payment_method_type',
            'total_amount',
            'tax_free_amount',
            'vat_amount',
            'approved_at',
            'status'
        )
        optional_fields = (
            'aid',
            'item_name',
            'quantity',
            'payment_method_type',
            'total_amount',
            'tax_free_amount',
            'vat_amount',
            'approved_at',
            )
        
    def update(self, instance, validated_data):
        return instance.set_status(**validated_data)

                

class ParticipationPaymentRequestSerializer(serializers.ModelSerializer):
    payment_result = PaymentResultSerializer(
        default = {
            'payment_method_type': PaymentMethod.MONEY,
            'item_name': Item.PICKUP_GAME,
            'status': PaymentStatus.READY,
            'quantity': 1,
            })
    
    class Meta:
        model = ParticipationPaymentRequest
        fields = (
            'participation', 
            'item_name', 
            'tax_free_amount',
            'vat_amount',
            'tid',
            'payment_result'
        )
        optional_fields = (
            'participation',
            'item_name', 
            'tax_free_amount',
            'vat_amount',
            'tid',
            'payment_result'
        )
        
    @transaction.atomic()
    def create(self, validated_data):
        """_summary_
        결제 결과와 결제 요청을 생성시키는 메소드
        
        """
        payment_result_data = validated_data.pop('payment_result')
        payment_result_obj = PaymentResult.objects.create(**payment_result_data)
        participation_data = validated_data['participation']
        instance = ParticipationPaymentRequest.objects.create(
            payment_result=payment_result_obj,
            partner_order_id=f'Participation#{participation_data.id}',
            partner_user_id=f'{participation_data.user_id}',
            quantity=1,
            total_amount=1*participation_data.game.fee,
            **validated_data
            )
        return instance
    
    def update(self, instance, validated_data):
        instance.tid = validated_data.get('tid', instance.tid)
        instance.save()
        return instance
        
        
        
        
        
        
    
            
        