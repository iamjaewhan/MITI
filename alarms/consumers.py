from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Alarm
from .serializers import AlarmSerializer

import json


async def get_alarms(user):
    return Alarm.objects.filter(participation__user=user)

async def get_serialized_alarms(alarms):
    serializer = AlarmSerializer(alarms, many=True)
    alarms.update(is_sent=True)
    return serializer.data
        
# @receiver(post_save, sender=Alarm)
# def detect_new_alarm(sender=Alarm, **kwargs):
#     print(kwargs)
#     print("signal is received comin from celery worker")


class AlarmConsumer(AsyncWebsocketConsumer):      
        
    async def connect(self):
        self.user = self.scope['user']
        self.channel_layer = get_channel_layer()
        self.group_name = str(self.user.username)
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        self.alarms = await get_alarms(self.user)
        serialized_alarms = await get_serialized_alarms(self.alarms)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_alarms',
                'alarm': serialized_alarms 
            }
        )
        
    async def send_alarms(self, event):
        data = event['alarm']
        await self.send(text_data=json.dumps({'alarm': data}))
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        alarm_id = data['alarm_id']
        checked_alarms = self.alarms.filter(id=alarm_id)
        checked_alarms.update(is_checked=True)
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        