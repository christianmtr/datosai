from rest_framework import permissions


class UserHasApiKeyPermission(permissions.BasePermission):
    message = 'Current user has not API Key.'

    def has_permission(self, request, view):
        user = request.user

        api_key = user.openai_api_key

        if api_key:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        api_key = user.openai_api_key

        if api_key:
            return True
        return False
