from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view()),
]
