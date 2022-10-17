from celery import shared_task

from alarms.models import Alarm
from games.models import Participation

@shared_task
def create_alarms(game_id):
    participations = Participation.objects.filter(game=game_id)
    for participation in participations:
        alarm, created = Alarm.objects.get_or_create(game=participation.game,
                             user=participation.user)
        if not created:
            alarm.set_unsent()
            
@shared_task
def delete_alarm(game_id, user_id):
    alarm = Alarm.objects.filter(game=game_id, user=user_id)
    alarm.delete()