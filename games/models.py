from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime, timedelta
from places.models import Place

# Create your models here.

class OpenedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_datetime__gt=datetime.now())
    
class ClosedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_datetime__lte=datetime.now())


class Game(models.Model):
    host = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    invitation = models.IntegerField(
        null=False,
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(255)
        ]
    )
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(auto_now_add=True)
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    info = models.CharField(max_length=255, null=True)
    
    objects = OpenedGameManager()
    closed_objects = ClosedGameManager()
    
    class Meta:
        ordering  = ['start_datetime']
    
    
    
        

    
    