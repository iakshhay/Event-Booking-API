from django.db import transaction
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from events.models import Event
from core.permissions import IsBookingOwner
from .models import Booking
from .serializers import BookingSerializer

# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class=BookingSerializer
    permission_classes=[IsAuthenticated,IsBookingOwner]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def create(self,request,*args,**kwargs):
        slug=kwargs.get('slug')

        with transaction.atomic():
            event=Event.objects.select_for_update() .get(slug=slug)

            serializer=self.get_serializer(
                data=request.data,
                context={'event':event}
            )

            serializer.is_valid(raise_exception=True)

            tickets=serializer.validated_data['tickets']
            if tickets>event.available_seats:
                return Response(
                    {'error':'Not enough seats available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            booking=serializer.save(
                user=request.user,
                event=event,
                status="confirmed"
            )

            event.available_seats-=tickets
            event.save()
        
        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        booking=self.get_object()

        with transaction.atomic():
            event=Event.objects.select_for_update().get(id=booking.event.id)

            event.available_seats += booking.tickets
            event.save()

            booking.status="cancelled"
            booking.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    