from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_check = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
        
        
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
        


