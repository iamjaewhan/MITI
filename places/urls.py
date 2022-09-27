from django.urls import path

from .views import *

urlpatterns = [
    path('', PlaceListView.as_view()),
    path('<int:place_id>/', PlaceDetailView.as_view()),
]
