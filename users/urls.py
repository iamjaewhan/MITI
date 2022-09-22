from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from dj_rest_auth.jwt_auth import get_refresh_view

from .views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('<int:user_id>/', UserUpdateView.as_view()),
    path('token/refresh/', get_refresh_view().as_view()),
    path('', UserListView.as_view()),
]
