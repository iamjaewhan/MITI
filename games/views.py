from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.serializers import BaseUserSerializer
from utils.permissions import IsOwner, IsParticipant

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


class PlayerListView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        objs = Participation.objects.filter(game_id=self.kwargs['game_id'])
        self.check_object_permissions(self.request, objs)
        return objs
    
    def get(self, request, game_id):
        queryset = self.get_queryset()
        objs = list(map(lambda x:x.user, queryset))
        serializer = BaseUserSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, game_id):
        try:
            data = {
                'game': game_id,
                'user': request.user.id
            }
            serializer = ParticipationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class PlayerDetailView(views.APIView):
    
    def get_object(self):
        obj = Participation.objects.get(game_id=self.kwargs['game_id'], user_id=self.kwargs['user_id'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsParticipant]
        elif self.request.method == 'DELETE':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
    
    def get(self, request, game_id, user_id):
        obj = self.get_object()
        serializer = BaseUserSerializer(obj.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, game_id, user_id):
        obj = self.get_object()
        serializer = ParticipationSerializer(obj)
        serializer.delete()
        return Response(status=status.HTTP_200_OK)
        
        