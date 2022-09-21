from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, objs):
        if request.user:
            for obj in objs:
                if obj.id == request.user.id:
                    return True
            raise PermissionDenied("해당 경기 참여자가 아닙니다.")
        raise NotAuthenticated("접근 권한이 없습니다.")
        