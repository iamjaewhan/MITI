from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.signals import request_finished

from .models import Alarm
from games.models import Participation, Game

import time

@receiver(post_save, sender=Game)
def create_alarm_objs(sender, **kwargs):
    if not kwargs['created'] and 'player' in kwargs['update_fields']:
        game = kwargs['instance']
        if game.is_fulfilled():
            for participation in Participation.objects.filter(game=game):
                obj, is_created = Alarm.objects.get_or_create(game=game, user=participation.user)
                if not is_created:
                    obj.is_sent = False
                    obj.save()
        
