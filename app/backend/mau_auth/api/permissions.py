from rest_framework import permissions


class DontAllowAnyone(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
