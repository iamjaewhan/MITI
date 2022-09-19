from rest_framework import views, status
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.

class GameListView(views.APIView):
    def get(self, request):
        queryset = Game.objects.all()
        serializer = BaseGameSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        