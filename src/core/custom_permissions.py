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


class IsOwnerOnly(BasePermission):
    """
    Custom permission to ensure the user can only access their own.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the instance belongs to the authenticated user
        """

        return obj.user == request.user


class IsAdminOrOwner(BasePermission):
    """
    Allows access only to admins or the owner of the object.
    """
    def has_permission(self, request, view):
        # Allow access if the user is authenticated and is an admin
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.user == request.user
