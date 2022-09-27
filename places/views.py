from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError


from .models import *
from .serializers import *

# Create your views here.

class PlaceListView(views.APIView):
    def get(self, request):
        """_summary_
        경기장 목록 조회 기능

        Returns:
            Response:
                200 : 요청 정상 처리
        """
        queryset = Place.objects.all()
        serializer = BasePlaceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """_summary_
        경기장 등록 기능

        Args:
            request :
                {
                    "name": "경기장 이름",
                    "address": "경기장 주소",
                    "address_detail": "경기장 상세 주소" (optional),
                    "contact": "경기장 연락처",
                    "info": "장소 정보" (optional) ,
                    "type": "장소 타입(실내,실외)"
                }

        Raises:
            ValidationError: 유효하지 않은 입력값 입력받은 경우

        Returns:
            Response:
                201 : 요청 정상 처리
        """
        serializer = BasePlaceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError("올바르지 않은 요청값입니다.")
    

class PlaceDetailView(views.APIView):
    def get(self, request, place_id):
        """_summary_
        경기장 상제 조회 기능

        Args:
            place_id (int): 조회할 경기장 id

        Raises:
            NotFound: 존재하지 않는 경기장 id일 경우

        Returns:
            Response:
                200 : 요청 정상 처리
        """
        queryset = Place.objects.filter(id=place_id)
        if queryset:
            serializer = BasePlaceSerializer(queryset[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound("유효하지 않은 요청값입니다.")
        
        