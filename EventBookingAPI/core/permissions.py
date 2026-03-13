from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "organizer"
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role=="organizer" and obj.organizer == request.user
