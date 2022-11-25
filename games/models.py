from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from places.models import Place

# Create your models here.

class OpenedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_datetime__gt=timezone.now()).order_by('-start_datetime')

    
class ClosedGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_datetime__lte=timezone.now()).order_by('-start_datetime')


class AllGameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-start_datetime')


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
    min_invitation = models.IntegerField(default=1, null=False)
    player = models.IntegerField(default=0, null=False)
    start_datetime = models.DateTimeField(default=timezone.now, null=False)
    end_datetime = models.DateTimeField(default=timezone.now, null=False)
    address = models.CharField(max_length=255, default='경기도 화성시 동탄대로 6길 20')
    info = models.CharField(max_length=255, null=True)
    
    objects = OpenedGameManager()
    closed_objects = ClosedGameManager()
    all_objects = AllGameManager()
    
    class Meta:
        ordering  = ['start_datetime']
        
    def is_fulfilled(self):
        return self.min_invitation == self.player
    
    @transaction.atomic()
    def increase_player(self):
        self.player += 1
        self.save(update_fields=['player'])
        
    @transaction.atomic()
    def decrease_player(self):
        self.player -= 1
        self.save(update_fields=['player'])
    
    
class Participation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'user'], name='unique participation')
        ]
            