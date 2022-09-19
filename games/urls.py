from django.urls import path

from .views import *

urlpatterns = [
    path('', GameListView.as_view()),
]
