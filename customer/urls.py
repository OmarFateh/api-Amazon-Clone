from django.urls import path

from .views import (UpdateDetailCustomerAPIView, AddressListAPIView, AddressCreateAPIView, AddressUpdateDeleteAPIView,
                    PaymentListAPIView, PaymentCreateAPIView, PaymentUpdateDeleteAPIView,
                    WishlistProductListAPIView)


"""
CLIENT
BASE ENDPOINT /api/customers/
"""

urlpatterns = [
    # Profile
    path('my-profile/', UpdateDetailCustomerAPIView.as_view(), name='customer-profile-detail-update'),
    # Address
    path('addresses/', AddressListAPIView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateAPIView.as_view(), name='address-create'),
    path('addresses/<str:address_uuid>/', AddressUpdateDeleteAPIView.as_view(), name='address-detail'),
    # Payment
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/<str:payment_uuid>/', PaymentUpdateDeleteAPIView.as_view(), name='payment-detail'),
    # Wishlist
    path('wishlist/', WishlistProductListAPIView.as_view(), name='wishlist-list'),
]