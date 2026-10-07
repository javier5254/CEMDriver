from rest_framework.permissions import BasePermission


def _has_role(user, *roles):
    return bool(user and user.is_authenticated and user.rol in roles)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, 'ADMIN')


class IsAlistador(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, 'ALISTADOR')


class IsMotorizado(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, 'MOTORIZADO')


class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, 'CLIENTE')
