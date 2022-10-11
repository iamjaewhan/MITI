from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Alarm
from .serializers import AlarmSerializer

import json


def get_alarms(user_id=None):
    if user_id:
        alarms = Alarm.objects.all().filter(user=user_id)
    else:
        alarms = Alarm.objects.all()
    serializer = AlarmSerializer(alarms, many=True)
    return serializer.data


class AlarmConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        async_to_sync(self.channel_layer.group_add)(
            self.user_id,
            self.channel_name
        )
        self.accept()
        
        alarms = get_alarms(self.user_id)
        async_to_sync(self.channel_layer.group_send)(self.user_id, {
                "type": "alarms",
                "data": alarms
            }
        )
        
    def disconnect(self, close_code):
        alarms = get_alarms(self.user_id)
        alarms.update(is_sent=True)

        async_to_sync(self.channel_layer.group_discard)(
            self.user_id,
            self.channel_name
        )
    
    def alarms(self, event):
        self.send(text_data=json.dumps(event))
        