from rest_framework.permissions import BasePermission

from constants.enums import RoleChoices


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False


class IsEmployee(BasePermission):
    """
    Custom permission to allow only admins or employees to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and has the required role
        return request.user.role in [
            RoleChoices.CANDIDATE,
            RoleChoices.EMPLOYEE,
        ]


class IsAdmin(BasePermission):
    """
    Custom permission to allow only admins to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and is an admin
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrOwner(BasePermission):
    """
    Allows access only to admins or the owner of the object.
    """
    def has_permission(self, request, view):
        # Allow access if the user is authenticated and is an admin
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.user == request.user
