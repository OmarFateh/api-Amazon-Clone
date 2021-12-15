from rest_framework import permissions


class IsMerchant(permissions.BasePermission):
    """A custom permission to allow only merchants to view/create an object."""
    message = "You have to be a merchant to apply action for this item."

    def has_permission(self, request, view):
        # User must be an merchant.
        if request.user.is_authenticated:
            return request.user.user_type == 'M'
        return False 


class IsMerchantOwner(IsMerchant):
    """
    Object-level permission to allow only merchants to edit/delete an object.
    Obj should has merchant attribute.
    """
    message = "You have to be a merchant & owner to apply action for this item."

    def has_object_permission(self, request, view, obj):
        return obj.merchant == request.user.merchant         