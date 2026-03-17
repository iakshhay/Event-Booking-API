from django.utils import timezone
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['title','description','language','event_type','location','city','max_capacity','available_seats','event_date_time','status','created_at']
        extra_kwargs={
            "slug":{"read_only":True},
            "available_seats":{"read_only":True},
            "status":{"read_only":True},
            "created_at":{"read_only":True}
        }

    def validate_event_date_time(self,value):
        if value<=timezone.now():
            raise serializers.ValidationError("Event date must be in future")
        return value

    def create(self, validated_data):
        user=self.context['request'].user
        return Event.objects.create(organizer=user,**validated_data)
