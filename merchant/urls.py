from django.urls import path

from .views import UpdateDetailMerchantAPIView, MerchantProductListAPIView


"""
CLIENT
BASE ENDPOINT /api/merchants/
"""

urlpatterns = [
    path('my-profile/', UpdateDetailMerchantAPIView.as_view(), name='merchant-profile-detail-update'),
    path('my-products/', MerchantProductListAPIView.as_view(), name='my-product-list'),
]