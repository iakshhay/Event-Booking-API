from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=[
            'id','user','event','tickets','status','created_at','updated_at'
            ]
        read_only_fields=[
            'id','user','event','status','created_at','updated_at'
        ]

    def validate_tickets(self,value):
        event=self.context.get('event')
        if value < 0:
            raise serializers.ValidationError("Tickets must be greater than 0.")
        if value > event.available_seats:
            raise serializers.ValidationError(f"Only {event.available_seats} are avaliable.")
        return value
    
    
