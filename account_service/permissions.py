from typing import Any
from rest_framework import permissions
from rest_framework.request import Request


class CanSuspendUserPermission(permissions.BasePermission):
    
    edit_methods = "You can not suspend a creator if you are not our staff!"
    method = ("PUT", "PATCH")
    
    def has_permission(self, request:Request, view:Any) -> bool:
        if request.user.is_authenticated and request.user.is_staff:
            return True
        
    def has_object_permission(self, request:Request, view:Any) -> bool:
        if request.method not in self.edit_methods and request.user.has_perm("user.can_suspend_user"):
            return True
        return False