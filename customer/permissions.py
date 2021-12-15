from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    """
    A custom permission to allow only customers to view/create an object.
    """
    message = "You have to be a customer to apply action for this item."

    def has_permission(self, request, view):
        # User must be a customer.
        if request.user.is_authenticated:
            return request.user.user_type == 'C'
        return False 


class IsCustomerOwner(IsCustomer):
    """
    Object-level permission to allow only customers to edit/delete an object.
    """
    message = "You have to be a customer & owner to apply action for this item."

    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user.customer