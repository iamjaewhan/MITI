from django.db import models
from django.utils.translation import gettext as _

from games.models import Participation

# Create your models here.
class Item(models.TextChoices):
    PICKUP_GAME = 'PG'


class PaymentStatus(models.TextChoices):
    READY = 'RD'
    APPROVED = 'AP'
    FAILED = 'FL'
    CANCELED = 'CL'
    
class PaymentMethod(models.TextChoices):
    CARD = 'CD'
    MONEY = 'MN'
    

class PaymentResult(models.Model):    
    aid = models.CharField(max_length=50, null=True, blank=True)
    item_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)

    payment_method_type = models.CharField(
        max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.MONEY)
    total_amount = models.IntegerField(
        verbose_name=_("결제 총액"), null=True, blank=True)
    tax_free_amount = models.IntegerField(
        verbose_name=_("상품 비과세 금액"), null=True, blank=True)
    vat_amount = models.IntegerField(
        verbose_name=_("상품 부과세 금액"), null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=PaymentStatus.choices, default=PaymentStatus.READY)
    
    approved_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class ParticipationPaymentRequest(models.Model):
    item_name = models.CharField(max_length=10, choices=Item.choices, default=Item.PICKUP_GAME)
    partner_order_id = models.CharField(max_length=30)
    partner_user_id = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)
    total_amount = models.IntegerField(verbose_name=_("결제 총액"))
    tax_free_amount = models.IntegerField(verbose_name=_("상품 비과세 금액"), default=0, blank=True)
    vat_amount = models.IntegerField(verbose_name=_("상품 부과세 금액"), default=0, blank=True) 
    tid = models.CharField(max_length=30, null=True, blank=True)
    
    participation = models.OneToOneField(Participation, on_delete=models.PROTECT)
    payment_result = models.OneToOneField(PaymentResult, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_request_at = models.DateTimeField(auto_now=True)
    
