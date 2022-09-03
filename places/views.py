from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response


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
        return Response(status=status.HTTP_400_BAD_REQUEST)