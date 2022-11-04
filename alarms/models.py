from django.db import models, transaction
from django.utils import timezone

from games.models import Participation

# Create your models here.

class AlarmManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_checked=False).filter(valid_until__gt=timezone.now())


class Alarm(models.Model):
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE)
    is_sent = models.BooleanField(null=False, default=False)
    is_checked = models.BooleanField(null=False, default=False)
    valid_until = models.DateTimeField(null=False, default=timezone.now)
    
    objects = AlarmManager()
    all_objects = models.Manager()
    
    @transaction.atomic()
    def set_unsent(self):
        self.is_sent = False
        self.is_checked = False
        self.save(update_fields=['is_sent', 'is_checked'])
        
    
