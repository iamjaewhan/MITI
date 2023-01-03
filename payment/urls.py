from django.urls import path

from games.views import *
from .views import *

urlpatterns = [
    path('requests/<int:payment_request_id>/approval/', KakaoPaymentApprovalCallbackView.as_view()),
    path('requests/<int:payment_request_id>/fail/', KakaoPaymentFailCallbackView.as_view()),
    path('requests/<int:payment_request_id>/cancel/', KakaoPaymentCancelCallbackView.as_view()),
]
