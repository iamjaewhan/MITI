from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from places.models import Place

# Create your models here.

class OpenedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_datetime__gt=timezone.now())

    
class ClosedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_datetime__lte=timezone.now())


class AllGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


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
    start_datetime = models.DateTimeField(default=timezone.now, null=False)
    end_datetime = models.DateTimeField(default=timezone.now, null=False)
    address = models.CharField(max_length=255, default='경기도 화성시 동탄대로 6길 20')
    info = models.CharField(max_length=255, null=True)
    
    objects = OpenedGameManager()
    closed_objects = ClosedGameManager()
    all_objects = AllGameManager()
    
    class Meta:
        ordering  = ['start_datetime']
    
    
    
        

    
    