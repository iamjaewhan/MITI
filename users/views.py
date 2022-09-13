from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *

# Create your views here.
class UserSignupView(views.APIView):
    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                serializer = BaseUserSerializer(instance=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class UserLoginView(views.APIView):
    def post(self, request):
        user = authenticate(email=request.data.get('email', None), password=request.data.get('password', None))
        if user:
            serializer = BaseUserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res_data = {
                "user": serializer.data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            return Response(data=res_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
class UserLogoutView(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token', None)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
