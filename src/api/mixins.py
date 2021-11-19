from rest_framework.permissions import BasePermission


class ChangeOnlyForOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id
