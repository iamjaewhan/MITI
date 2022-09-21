from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.
class GameListView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Game.objects.all()
        serializer = BaseGameSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['host'] = request.user.id
        serializer = GameRegisterSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status.status.HTTP_400_BAD_REQUEST)        
        
        
