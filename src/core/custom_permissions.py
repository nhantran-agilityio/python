from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    """
    Custom permission to allow only admins or employees to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and has the required role
        return (
            request.user.is_authenticated and
            request.user.role in ['candidate', 'employee']
        )


class IsAdmin(BasePermission):
    """
    Custom permission to allow only admins to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and is an admin
        return request.user.is_authenticated and request.user.role == 'admin'
