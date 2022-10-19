from rest_framework import serializers

from .models import Alarm


class AlarmSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Alarm
        fields = ['id', 'user', 'game', 'is_sent', 'is_checked', 'valid_until']
        
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        game_id = representation.pop('game')
        representation['game_id'] = game_id
        representation['game_host'] = obj.game.host.email
        representation['game_start_datetime'] = str(obj.game.start_datetime)
        return representation