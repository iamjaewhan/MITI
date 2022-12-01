from django.db import models
from django.utils.translation import gettext as _

from games.models import Participation

# Create your models here.
class ParticipationPaymentRequest(models.Model):
    tid = models.CharField(max_length=30, unique=True)
    item_code = models.CharField(max_length=30, null=True, blank=True)
    participation = models.OneToOneField(Participation, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    total_amount = models.IntegerField(verbose_name=_("결제 총액"))
    tax_free_amount = models.IntegerField(verbose_name=_("상품 비과세 금액"), default=0, blank=True)
    vat_amount = models.IntegerField(verbose_name=_("상품 부과세 금액"), default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_request_at = models.DateTimeField(auto_now=True)