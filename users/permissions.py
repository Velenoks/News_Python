from rest_framework import permissions


class AdminOnlyPermission(permissions.BasePermission):
    """Проверка на Администратора."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.is_superuser)


class AdminOrAuthorPermission(permissions.BasePermission):
    """Проверка на Администратора и Пользователя."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or obj.username == request.user.username)
