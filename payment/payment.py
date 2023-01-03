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
    
class KakaoPayApprovalDto:
    model = ParticipationPaymentRequest
    required_param_keys = ('tid', 'partner_order_id', 'partner_user_id', 'pg_token')
    params = {
        'cid': getattr(settings, "KAKAO_CID"),
    }

    def __init__(self, obj : ParticipationPaymentRequest, pg_token=None):
        assert isinstance(obj, KakaoPayApprovalDto.model), '해당 모델로는 요청을 생성할 수 없습니다.'

        self.set_params(obj)
        self.set_param('payment_request', obj.id)
        self.set_param('pg_token', pg_token)
        
    def set_params(self, obj : ParticipationPaymentRequest):
        for key in self.required_param_keys:
            self.params[key] = getattr(obj, key, None)
            
    def set_param(self, key, value):
        self.params[key] = value
            
    def set_response(self, kwargs):
        for key in kwargs.keys():
            if key == "amount":
                for k_key in kwargs[key].keys():
                    self.params[k_key+"_"+key] = kwargs[key][k_key]
            else:
                self.params[key] = kwargs.get(key, self.params.get(key, None))
        
    def get_params(self):
        return self.params
        
        

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
        
        
