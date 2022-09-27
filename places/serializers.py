from rest_framework import serializers

from .models import *

class BasePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        
    def create(self, validated_data):
        """_summary_
        유효성 검증을 마친 데이터를 사용하여 place 모델의 create() 호출

        Args:
            validated_data : 유효성 검증이 끝난 fields 의 dictionary

        Returns:
            생성된 place 객체
        """
        instance = Place.objects.create(**validated_data)
        return instance