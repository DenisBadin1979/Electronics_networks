from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Доступ только для активных сотрудников (is_active=True и is_staff=True).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            request.user.is_staff
        )