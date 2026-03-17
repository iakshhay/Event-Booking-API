from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Event
from .serializers import EventSerializer
from core.permissions import IsOrganizer, IsOwnerOrganizer

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    lookup_field="slug"
    filterset_fields=['city', 'event_type', 'language', 'status']
    search_fields=['title','description','location']
    ordering_fields=['event_date_time','created_at']

    permission_classes_by_action={
        'list':[AllowAny],
        'create':[IsAuthenticated, IsOrganizer],
        'update':[IsAuthenticated, IsOwnerOrganizer],
        'retrieve':[AllowAny],
        'partial_update':[IsAuthenticated, IsOwnerOrganizer],
        'destroy':[IsAuthenticated, IsOwnerOrganizer]
    }

    def get_permissions(self):
        permission_classes=self.permission_classes_by_action.get(
            self.action,
            self.permission_classes
        )
        return[permission() for permission in permission_classes]
    