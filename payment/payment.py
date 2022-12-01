from django.conf import settings

from games.models import Participation

class KakaoPayReadyRequest:
    data = {
        'cid': getattr(settings, "KAKAO_CID"),
    }
    
    def __init__(self, obj : Participation):
        self.obj = obj
        self.set_data() 
    
    def set_data(self):
        if isinstance(self.obj, Participation):
            self.data['partner_order_id'] = self.obj.id
            self.data['partner_user_id'] = self.obj.user.id
            self.data['item_name'] = f'경기 참여 - {self.obj.id}'
            self.data['quantity'] = 1
            self.data['total_amount'] = self.data['quantity'] * self.obj.game.fee
            self.data['tax_free_amount'] = 0
            self.data['approval_url'] = getattr(settings, "KAKAO_APPROVAL_URL")%(self.obj.game.id, self.obj.user.id)
            self.data['fail_url'] = getattr(settings, "KAKAO_FAIL_URL")%(self.obj.game.id, self.obj.user.id)
            self.data['cancel_url'] = getattr(settings, "KAKAO_CANCEL_URL")%(self.obj.game.id, self.obj.user.id)
            
    def set_response(self, kwargs):
        kwargs.pop('created_at')
        for key in kwargs.keys():
            self.data[key] = kwargs.get(key, self.data.get(key, None))
            
    def get_data(self):
        return self.data
        

import requests

       
class KakaoPayClient:
    ADMIN_KEY = getattr(settings, "KAKAO_ADMIN_KEY")
    READY_URL = getattr(settings, "KAKAO_PAY_READY_URL")
    
    headers = {
        "Authorization": "KakaoAK " + f"{ADMIN_KEY}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    
    def ready(self, params: KakaoPayRequestParameter):
        res = requests.post(
            self.READY_URL, headers=self.headers, params=params.get_data()
        )
        params.set_response(res.json())    
        return params`
        
        
