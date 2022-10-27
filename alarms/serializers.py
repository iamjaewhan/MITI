from rest_framework import serializers

from .models import Alarm


class AlarmSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Alarm
        fields = ['id','participation' ,'is_sent', 'is_checked', 'valid_until']
        
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        participation = representation.pop('participation')
        representation['game_id'] = obj.participation.game.id
        representation['game_host'] = obj.participation.game.host.email
        representation['user_email'] = obj.participation.user.email
        representation['user_id'] = obj.participation.user.id
        representation['game_start_datetime'] = str(obj.participation.game.start_datetime)
        return representation