from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to allow only admins to modify data.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Only admin users (staff) can modify