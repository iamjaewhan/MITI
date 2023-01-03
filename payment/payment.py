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
    

class KakaoPayReadyDto(KakaoPayDto):
    required_parameters = ('partner_order_id', 'partner_user_id', 'quantity', 'total_amount', 'tax_free_amount', 'item_name')

    def __init__(self, obj:ParticipationPaymentRequest):
        assert isinstance(obj, ParticipationPaymentRequest), '해당 모델로는 요청을 생성할 수 없습니다.' 
        
        for param in self.required_parameters:
            self.add_param(param, getattr(obj, param, None))
        self.set_urls(obj)
            
    def set_urls(self, obj):
        self.parameters['approval_url'] = getattr(
            settings, "KAKAO_APPROVAL_URL")%(obj.id)
        self.parameters['cancel_url'] = getattr(
            settings, "KAKAO_FAIL_URL")%(obj.id)
        self.parameters['fail_url'] = getattr(
            settings, "KAKAO_CANCEL_URL")%(obj.id)
            
    
class KakaoPayApprovalDto(KakaoPayDto):
    required_parameters = ('tid', 'partner_order_id', 'partner_user_id', 'pg_token')
    response_parameters = ('aid', 'amount', 'approved_at')

    def __init__(self, obj : ParticipationPaymentRequest):
        assert isinstance(obj, ParticipationPaymentRequest), '해당 모델로는 요청을 생성할 수 없습니다.'

        for param in self.required_parameters:
            self.add_param(param, getattr(obj, param, None))
    
    def get_flatten(self):
        return self.flatten(self.get_params())
            
    def flatten(self, data, prefix='', sep='_'):
        items = []
        for k, v in data.items():
            new_key = k + sep + prefix if prefix else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten(data=v, prefix=new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

        
        

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
            self.READY_URL, headers=self.headers, params=params.get_params())
        if res.status_code == 200:
            params.read_response(**res.json())    
            return params
        raise RequestFailException()
        
    def approve(params):        
        res = requests.post(
            KakaoPayClient.APPROVE_URL, headers=KakaoPayClient.headers, params=params.get_params()
        )
        
        params.set_response(res.json())
        print(params.get_params())
        return params
        
        
