from django.shortcuts import render, get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from utils.permissions import IsOwner

from .serializers import *

# Create your views here.
class UserSignupView(views.APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            serializer = BaseUserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
class UserLoginView(views.APIView):
     
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)    
    
    
class UserLogoutView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh', None)
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class UserUpdateView(views.APIView):
    permission_classes = [IsOwner]

    def get_object(self):
        obj = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, user_id):
        try:
            user = self.get_object()
            if user:
                serializer = BaseUserSerializer(user)
                if serializer.delete():
                    return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, user_id):
        try:
            user = self.get_object()
            if user:
                serializer = UserUpdateSerializer(user, data=request.data)
                if serializer.is_valid():
                    updated_user = serializer.save()
                    return Response(BaseUserSerializer(updated_user).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, user_id):
        try:
            user = self.get_object()
            if user:
                serializer = BaseUserSerializer(user)
                if serializer.restore():
                    return Response(serializer.data ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
    

class UserListView(views.APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        queryset = get_user_model().objects.all()
        serializer = BaseUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)