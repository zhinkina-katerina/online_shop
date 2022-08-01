from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class OnlyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer.user == request.user
