from django.db import models
from django.contrib.auth import get_user_model

from games.models import Game

# Create your models here.

class AlarmManager(models.Manager):
    def get_queryset(slef):
        return super().get_queryset().filter(is_sent=False)


class Alarm(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_sent = models.BooleanField(null=False, default=False)
    
    objects = AlarmManager()
