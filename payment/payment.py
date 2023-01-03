from django.conf import settings

from games.models import Participation
from payment.models import ParticipationPaymentRequest, PaymentStatus, PaymentMethod

from constants.custom_exceptions import (
    RequestFailException,
)



class KakaoPayDto:
    parameters = {
        'cid' : getattr(settings, "KAKAO_CID")
    }
    
    def get_params(self):
        return self.parameters
    
            
    def add_param(self, key, value):
        self.parameters[key] = value
        
    def read_response(self, **kwargs):
        for key in kwargs.keys():
            self.add_param(key, kwargs[key])
    


        
            
            
            else:
        
        

import requests

       
class KakaoPayClient:
    ADMIN_KEY = getattr(settings, "KAKAO_ADMIN_KEY")
    READY_URL = getattr(settings, "KAKAO_PAY_READY_URL")
    APPROVE_URL = getattr(settings, "KAKAO_PAY_APPROVAL_URL")
    
    headers = {
        "Authorization": "KakaoAK " + f"{ADMIN_KEY}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    
    
    def ready(self, params):
        res = requests.post(
            self.READY_URL, headers=self.headers, params=params.get_params()
        )
        params.read_response_data(**res.json())    
        return params
        
    def approve(params):        
        res = requests.post(
            KakaoPayClient.APPROVE_URL, headers=KakaoPayClient.headers, params=params.get_params()
        )
        
        params.set_response(res.json())
        print(params.get_params())
        return params
        
        
