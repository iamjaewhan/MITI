from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Participation, Game
from .tasks import create_alarms, delete_alarm


@receiver(post_save, sender=Participation)
def _post_save_receiver(sender, instance, created, **kwargs):
    if created:
        game = instance.game
        game.increase_player()
        if game.is_fulfilled():
            create_alarms.delay(game.id)
            
@receiver(post_delete, sender=Participation)
def _post_delete_receiver(sender, instance, **kwargs):
    game = instance.game
    game.decrese_player()
    delete_alarm.delay(instance.game.id, instance.user.id)
    