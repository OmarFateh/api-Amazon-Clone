from django.urls import path

from .views import OrderListCreateAPIView, OrderUpdateDeleteAPIView, CouponListCreateAPIView, CouponUpdateDeleteAPIView


"""
CLIENT
BASE ENDPOINT /api/orders/
"""

urlpatterns = [
    # order 
    path('', OrderListCreateAPIView.as_view(), name='orders-list-create'),
    path('<int:order_id>/', OrderUpdateDeleteAPIView.as_view(), name='orders-update-delete'),
    # Coupon
    path('coupons/', CouponListCreateAPIView.as_view(), name='coupons-list-create'),
    path('coupons/<int:coupon_id>/', CouponUpdateDeleteAPIView.as_view(), name='coupons-update-delete'),
]