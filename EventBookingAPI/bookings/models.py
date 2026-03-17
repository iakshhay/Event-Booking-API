from django.db import models
from django.db.models import Q
from users.models import User
from events.models import Event

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled')
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookings')
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='bookings')
    tickets=models.PositiveIntegerField()
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['user','event'],
                                    condition=~Q(status='cancelled'),
                                    name="unique_event_booking_for_active_bookings")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    