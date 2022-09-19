from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from datetime import datetime

from .validations import UserPasswordValidator

class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_check = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    def validate_password(self, value):
        return UserPasswordValidator.check_password(value)
        
        
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username']
        
    def delete(self):
        try:
            with transaction.atomic():
                self.instance.deleted_at = datetime.now()
                self.instance.save()
                return True
        except Exception:
            return False
        
    def restore(self):
        try:
            with transaction.atomic():
                self.instance.deleted_at = None
                self.instance.save()
                return True
        except Exception:
            return False
        

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'new_password']
        
    def validate_password(self, value):
        if not check_password(value, self.instance.password):
            raise ValueError("잘못된 비밀번호입니다.")
        return value
        
    def validate_new_password(self, value):
        UserPasswordValidator.check_password(value)
        return value
    
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                instance.email = validated_data.get('email', instance.email)
                instance.username = validated_data.get('username', instance.username)
                instance.username = validated_data.get('username', instance.username)
                new_password = validated_data.get('new_password', None)
                if new_password:
                    instance.set_password(new_password)
                instance.save()
                return instance
        except Exception:
            raise ValueError()

        


        
        
        
        



