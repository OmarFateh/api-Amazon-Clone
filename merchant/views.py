from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from product.serializers import ProductListSerializer
from product.models import Product
from .models import Merchant
from .serializers import MerchantDetailSerializer
from .permissions import IsMerchant, IsMerchantOwner


###
# Profile
###
class UpdateDetailMerchantAPIView(generics.RetrieveUpdateAPIView):
    """
    Update detail merchant profile API view.
    Only merchant can access his data and update it.
    """
    permission_classes = [IsMerchant]
    queryset = Merchant.objects.all()
    serializer_class = MerchantDetailSerializer
    
    def get_object(self, *args, **kwargs):
        # get current merchant user.
        obj = get_object_or_404(Merchant, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


###
# Product
###
class MerchantProductListAPIView(generics.ListAPIView):
    """Merchant Product list API view."""
    permission_classes = [IsMerchant]
    serializer_class = ProductListSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the products
        for the currently authenticated merchant.
        """
        return Product.objects.filter(merchant=self.request.user.merchant)