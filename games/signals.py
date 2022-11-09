from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Participation, Game
from .tasks import create_alarms, delete_alarm


@receiver(post_save, sender=Participation)
def _post_save_receiver(sender, instance, created, **kwargs):
    """_summary_
    Participation 모델의 signal receiver
    참여가 발생한 경기의 player 수를 증가시키고 최소 인원 모집이 완료된 경우
    알람 생성하는 비동기 태스크를 실행한다.

    Args:
        instance (Participation): save된 participation 객체
        created (boolean): 객체 생성 여부 
    """
    if created:
        game = instance.game
        game.increase_player()
        if game.is_fulfilled():
            create_alarms.delay(game.id)
            
@receiver(post_delete, sender=Participation)
def _post_delete_receiver(sender, instance, **kwargs):
    """_summary_
    Participation 모델의 signal receiver
    참여가 취소된 경기의 player 수를 감소시키고
    해당 참여 기록에 해당하는 참여자의 알람을 삭제한다.

    Args:
        instance (participation): delete된 participation 객체
    """
    game = instance.game
    game.decrease_player()
    if game.player < game.min_invitation:
        delete_alarm.delay(instance.game.id, instance.user.id)
    