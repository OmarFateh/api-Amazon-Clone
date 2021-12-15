from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from category.permissions import IsAdmin
from customer.permissions import IsCustomer, IsCustomerOwner
from .models import Order, OrderItem, Coupon
from .serializers import OrderSerializer, CouponSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    """
    Customer Order create API view.
    Only a customer can create it.
    """
    permission_classes = [IsCustomer]
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the orders
        for the currently authenticated customer.
        """
        return Order.objects.select_related('customer__user').filter(customer=self.request.user.customer)    

    def perform_create(self, serializer):
        """Set authenticated customer to be the order's customer automatically."""
        serializer.save(customer=self.request.user.customer)

    def get_serializer_context(self, *args, **kwargs):
        return {"is_update": False}


class OrderUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Customer Order update delete API view.
    Only the authenticated customer owner can update or delete it.
    """
    permission_classes = [IsCustomerOwner]
    serializer_class = OrderSerializer

    def get_object(self, *args, **kwargs):
        # get order id from the requested url.
        order_id = self.kwargs.get("order_id", None)
        customer = self.request.user.customer
        obj = get_object_or_404(Order, id=order_id, customer=customer)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the orders
        for the currently authenticated customer.
        """
        return Order.objects.select_related('customer__user').filter(customer=self.request.user.customer)      

    def get_serializer_context(self, *args, **kwargs):
        return {"is_update":True, 'order_obj': self.get_object()}

        
###
# Coupon
###
class CouponListCreateAPIView(generics.ListCreateAPIView):
    """Coupon list create API view."""
    permission_classes = [IsAdmin]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"is_create":True}


class CouponUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Coupon detail update delete API view. 
    Only the admin can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [IsAdmin]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def get_object(self, *args, **kwargs):
        # get coupon id from the requested url.
        coupon_id = self.kwargs.get("coupon_id", None)
        obj = get_object_or_404(Coupon, id=coupon_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self, *args, **kwargs):
        return {"coupon":self.get_object(), "is_create":False}