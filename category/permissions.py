from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """A custom permission to allow only admins to create/edit/delete an object."""
    message = "You have to be an admin to apply action for this item."

    def has_permission(self, request, view):
        # User must be an admin.
        if request.user.is_authenticated:
            return request.user.user_type == 'A'
        return False