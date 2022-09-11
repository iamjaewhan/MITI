from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response


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