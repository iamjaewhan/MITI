from django.db import transaction
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from utils.fields import PasswordField
from utils.validators import BaseTokenValidator

class UserSignupSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_check = PasswordField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'password_check']
    
    def validate(self, data):
        """_summary_
        password, password_check 일치 검사

        Raises:
            serializers.ValidationError: password, password_check 값이 일치하지 않는 경우
        """
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data
    
    def create(self, validated_data):
        """_summary_
        validated_data로 user 인스턴트 생성 및 DB 저장
        """      
        user = get_user_model().objects.create_user(**validated_data)
        return user
        
        
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username']
        
    def delete(self):
        self.instance.set_deleted_at()
            
    def restore(self):
        self.instance.set_deleted_at_null()
        

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = PasswordField(required=True, write_only=True)
    new_password = PasswordField(required=False, write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'new_password']
        
    def validate_password(self, value):
        if not check_password(value, self.instance.password):
            raise serializers.ValidationError("잘못된 비밀번호입니다.")
        return value
    
    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance
        
        
class UserLoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    password = PasswordField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    def validate(self, data):
        """_summary_
        입력받은 email, password로 회원정보 확인 후 access, refresh token을 data에 추가. -> 분리 필요.
        
        Raises:
            AuthenticationFailed: email,password 일치하는 회원 없는 경우
        return:
            data:
                {
                    "email": "유저 이메일",
                    "access": "access token 문자열",
                    "refresh": "refresh token 문자열"
                }
        """
        user = authenticate(email=data.get('email', None), password=data.get('password', None))
        if user:
            token = TokenObtainPairSerializer.get_token(user)
            data['id'] = user.id
            data['access'] = str(token.access_token)
            data['refresh'] = str(token)
            return data
        raise AuthenticationFailed('잘못된 로그인 정보입니다.')
    

class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True, validators=[BaseTokenValidator(),])
    message = serializers.CharField(read_only=True)
    
    def logout(self):
        """_summary_
        request body에 있는 refresh token을 blacklist에 추가하여 로그아웃

        Returns:
            data:
                {
                    "message": "로그아웃되었습니다."
                }
        """
        token = self.validated_data.get('refresh', None)
        refresh_token = RefreshToken(token)
        refresh_token.blacklist()
        self.validated_data['message'] = '로그아웃되었습니다.'
        return validated_data
        


        


        
        
        
        



