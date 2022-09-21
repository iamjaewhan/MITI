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
        
        
class GameDetailView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, game_id):
        try:
            game_instance = Game.objects.get(id=game_id)
            if game_instance:
                serializer = GameDetailSerializer(game_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)                
