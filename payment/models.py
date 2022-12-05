from django.db import models
from django.utils.translation import gettext as _

from games.models import Participation

# Create your models here.
ITEM_NAME = (
    ("PG", _("PICKUP GAME")),
)

class ParticipationPaymentRequest(models.Model):
    ##요청필수
    item_name = models.CharField(max_length=30, choices=ITEM_NAME, default="PG")
    partner_order_id = models.CharField(max_length=30)
    partner_user_id = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)
    total_amount = models.IntegerField(verbose_name=_("결제 총액"))
    tax_free_amount = models.IntegerField(verbose_name=_("상품 비과세 금액"), default=0)
    
    vat_amount = models.IntegerField(verbose_name=_("상품 부과세 금액"), default=0, blank=True) 
    #응답
    tid = models.CharField(max_length=30, null=True, blank=True)
    
    participation = models.OneToOneField(Participation, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_request_at = models.DateTimeField(auto_now=True)