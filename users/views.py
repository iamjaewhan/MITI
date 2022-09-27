from django.shortcuts import render, get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound, MethodNotAllowed

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
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.logout()
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class UserUpdateView(views.APIView):
    
    def get_queryset(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return get_user_model().objects.all()
        elif self.request.method == 'PUT':
            return get_user_model().deleted_objects.all()
        raise MethodNotAllowed()
              
    def get_permissions(self):
        """_summary_
        요청에 따른 permission_class 설정
        유저 삭제, 수정 : 요청을 보낸 사용자가 삭제,수정 대상 유저인지 확인하는 class로 설정
        유저 정보 복구 : 관리자 사용자 권한으로 설정

        """
        permission_classes = []
        if self.request.method in ['DELETE', 'PATCH']:
            permission_classes = [IsOwner]
        elif self.request.method == 'PUT':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self):
        """_summary_
        요청을 처리할 대상인 객체를 반환하는 메소드.
        path variable로 주어진 user_id로 user 인스턴스를 찾아 permission 검증 진행

        Returns:
            User 인스턴스
        """
        obj = get_object_or_404(self.get_queryset(), id=self.kwargs['user_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, user_id):
        """_summary_
        회원 탈퇴 : deleted_at 속성에 요청 시간을 입력하여 soft delete

        Args:
            user_id (int): 삭제할 유저의 id

        Raises:
            NotFound: 존재하지 않는 유저/이미 삭제된 유저의 id인 경우
        Returns:
            Response:
                200 : 요청 정상 처리
        """
        user = self.get_object()
        if user:
            serializer = BaseUserSerializer(user)
            serializer.delete()
            return Response(status=status.HTTP_200_OK)
        raise NotFound("일치하는 회원이 존재하지 않습니다.")

    def patch(self, request, user_id):
        """_summary_
        회원 정보 수정 
        
        Args:
            user_id (int): 삭제할 유저의 id 
            request : 
            {
                "email": "변경할 이메일"(optional),
                "username": "변경할 유저명"(optional),
                "password": "현재 비밀번호",
                "new_password": "새로운 비밀번호"(optional)
            }

        Raises:
            NotFound: 존재하지 않는 유저/이미 삭제된 유저의 id인 경우

        Returns:
            Response:
                200 : 요청 정상 처리
        """
        user = self.get_object()
        if user:
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                updated_user = serializer.save()
                return Response(BaseUserSerializer(updated_user).data, status=status.HTTP_200_OK)
        raise NotFound("일치하는 회원이 존재하지 않습니다.")
    
    def put(self, request, user_id):
        """_summary_
        탈퇴 회원 복구 : deleted_at 속성값을 초기화시켜 복구

        Args:
            user_id (int): 삭제할 유저의 id

        Raises:
            NotFound: 존재하지 않는 유저/삭제되지 않은 유저의 id인 경우
        Returns:
            Response:
                200 : 요청 정상 처리
        """
        user = self.get_object()
        if user:
            serializer = BaseUserSerializer(user)
            serializer.restore()
            return Response(serializer.data ,status=status.HTTP_200_OK)
        raise NotFound("일치하는 탈퇴 회원이 존재하지 않습니다.")
    

class UserListView(views.APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        queryset = get_user_model().objects.all()
        serializer = BaseUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)