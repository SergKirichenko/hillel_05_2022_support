from rest_framework.permissions import BasePermission

from authentication.models import DEFAULT_ROLES


class OperatorOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.role.id == DEFAULT_ROLES["admin"]:
            return True

        return False


class ClientOnly(BasePermission):
    def has_permission(self, request, view=None) -> bool:
        if request.user.role.id == DEFAULT_ROLES["user"]:
            return True

        return False


class PermissionTicketDelete(BasePermission):
    # Note: Permission allows user's to delete tickets, before oparator taken it.
    #       And allow admin's to delete tickets after them resolved is True.
    def has_object_permission(self, request, view, obj):
        user_role = request.user.role.id
        view = obj

        if user_role == DEFAULT_ROLES["user"]:
            if view.resolved is False and view.operator is None:
                return True
        elif user_role == DEFAULT_ROLES["admin"] and view.resolved is True:
            if request.user.id == view.operator.id:
                return True
        return False
