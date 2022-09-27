from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


from .models import *
from .serializers import *

# Create your views here.

class PlaceListView(views.APIView):
    def get(self, request):
        queryset = Place.objects.all()
        serializer = BasePlaceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BasePlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)class PlaceDetailView(views.APIView):
    def get(self, request, place_id):
        queryset = Place.objects.filter(id=place_id)
        if queryset:
            serializer = BasePlaceSerializer(queryset[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound("유효하지 않은 요청값입니다.")
        
        