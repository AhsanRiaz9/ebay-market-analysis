from rest_framework import permissions


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Get the user from the request
        user = request.user
        # print(user)
        # print(user.role.permissions.all())

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return False

        # Get the required permission code from the view
        required_permission_code = (
            view.allowed_permission() if hasattr(view, "allowed_permission") else None
        )

        if required_permission_code is None:
            return True  # No specific permission required for this view

        # Check if the user's role has the required permission
        return user.role.permissions.filter(code=required_permission_code).exists()
