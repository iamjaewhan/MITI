from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, 

class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user:
            if obj.id == request.user.id:
                return True
            raise PermissionDenied()
        raise NotAuthenticated()
        