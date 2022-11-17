from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Alarm
from .serializers import AlarmSerializer

import json


async def get_alarms(user):
    return Alarm.objects.filter(user=user)

async def get_serialized_alarms(alarms):
    serializer = AlarmSerializer(alarms, many=True)
    return serializer.data

# @receiver(post_save, sender=Alarm)
# def post_save_receiver(sender, instance, created, update_fields, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         group_name = str(instance.user.username)
#         async_to_sync(channel_layer.group_send)(
#             group_name, {
#                 'type': 'end_alarms',
#                 'data': get_serialized_alarms(instance)
#             }
#         )


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
        self.alarms.update(is_sent=True)
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
        