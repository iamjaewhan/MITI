from django.conf import settings
from games.models import Participation


class KakaoPayRequestParameter:
    data = {
        'cid': getattr(settings, "KAKAO_CID"),
        'approval_url': getattr(settings, "KAKAO_APPROVAL_URL"),
        'fail_url': getattr(settings, "KAKAO_FAIL_URL"),
        'cancel_url': getattr(settings, "KAKAO_CANCEL_URL"),
    }
    
    def __init__(self, obj):
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
            
    def set_response(self, kwargs):
        for key in kwargs.keys():
            self.data[key] = kwargs.get(key, self.data.get(key, None))
            
    def get_data(self):
        return self.data
        


        
        
