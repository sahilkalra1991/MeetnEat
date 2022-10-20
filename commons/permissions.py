from rest_framework.permissions import BasePermission


class IsMobileAppAdmin(BasePermission):
    """
    Example Permission class
    """

    def has_permission(self, request, view):
        return True
