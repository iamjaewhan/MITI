from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from dj_rest_auth.jwt_auth import get_refresh_view

from .views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('<int:user_id>/', UserUpdateView.as_view(), name='user_update'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('', UserListView.as_view(), name=''),
]
