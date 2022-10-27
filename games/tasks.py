from celery import shared_task

from alarms.models import Alarm
from games.models import Participation

@shared_task
def create_alarms(game_id):
    """_summary_
    특정 경기 참여자들의 알람을 생성하는 task

    Args:
        game_id (integer): 알람을 생성할 경기 Id
    """
    participations = Participation.objects.filter(game=game_id)
    for participation in participations:
        alarm, created = Alarm.objects.get_or_create(
            participation=participation,
            valid_until=participation.game.start_datetime
            )
        if not created:
            alarm.set_unsent()
            
@shared_task
def delete_alarm(game_id, user_id):
    """_summary_
    특정 알람을 삭제하는 task

    Args:
        game_id (integer): 경기 Id
        user_id (integer): 참여자 Id
    """
    participations = Participation.objects.filter(game=game_id, user=user_id)
    for participation in participations:
        alarm = Alarm.objects.filter(participation=participation)
        alarm.delete()    