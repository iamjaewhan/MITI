from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated


class IsParticipant(BasePermission):    
    def has_object_permission(self, request, view, obj):
        """_summary_
        특정 경기에 참여한 경기-참여자 관계 인스턴스 접근권한 class
        해당 경기에 참여한 사용자의 경우 True 반환

        Args:
            request : request 객체
            view : view 객체
            objs : Participation 객체

        Raises:
            PermissionDenied: 해당 객체들에 관하여 접근 권한이 없을때(자신의 경기 참여 기록이 아닐 경우).
            NotAuthenticated: 인증된 사용자가 아닌 경우

        Returns:
            boolean : 사용자와 participation의 user가 같은 obj가 존재하는 경우 True
        """
        if request.user:
            if obj.user == request.user:
                return True
            raise PermissionDenied("해당 참여자가 아닙니다.")
        raise NotAuthenticated("접근 권한이 없습니다.")
        

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """_summary_
        인스턴스 접근 권한 class
        객체의 user와 요청을 보낸 사용자가 일치하는지 확인한다.

        Args:
            request : request 객체
            view : check_object_permission()호출한 view 객체
            obj : User 객체

        Raises:
            PermissionDenied: User 객체와 request 보낸 사용자가 불일치 하는 경우
            NotAuthenticated: 인증된 사용자가 아닌 경우

        Returns:
            boolean : User 객체와 request 보낸 사용자가 불일치 하는 경우 True
        """
        if request.user:
            if obj.user == request.user:
                return True
            raise PermissionDenied()
        raise NotAuthenticated()