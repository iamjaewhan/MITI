from django.urls import path

from .views import *

urlpatterns = [
    path('', GameListView.as_view()),
    path('<int:game_id>/', GameDetailView.as_view()),
    path('<int:game_id>/players/', PlayerListView.as_view()),
    path('<int:game_id>/players/<int:user_id>/', PlayerDetailView.as_view()),
]
