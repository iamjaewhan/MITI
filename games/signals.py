from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from .models import Participation


@receiver(post_save, sender=Participation)
def _post_save_receiver(sender, instance, created, **kwargs):
    if created:
        game = instance.game
        game.player -= 1
        game.save(update_fields=['player'])
    

        
@receiver(pre_delete, sender=Participation)
def _pre_delete_receiver(sender, instance, **kwargs):
    game = instance.game
    print(kwargs)
    game.player -= 1
    game.save(update_fields=['player'])