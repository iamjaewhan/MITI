from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Participation, Game


@receiver(post_save, sender=Participation)
def _post_save_receiver(sender, **kwargs):
    game = kwargs['instance'].game
    game.player += 1
    game.save(update_fields=['player'])
        
@receiver(post_delete, sender=Participation)
def _post_delete_receiver(sender, **kwargs):
    game = kwargs['instance'].game
    game.player -= 1
    game.save(update_fields=['player'])