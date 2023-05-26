from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return False


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    """
    Grants the rights to edit for Admin, Moderator
    and Author of reviews and comments.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsAdministrator(BasePermission):
    """
    Grants the rights to all actions for Admin (and Superuser).
    """
    def has_permission(self, request, view):
        return (request.user.is_admin or request.user.is_superuser)
