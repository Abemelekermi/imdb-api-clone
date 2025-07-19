from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow object owner to edit/delete; others only read."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
