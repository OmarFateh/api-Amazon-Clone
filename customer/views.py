from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from product.serializers import WishlistProductListSerializer
from product.models import Wishlist
from .models import Customer, Address, Payment
from .permissions import IsCustomer, IsCustomerOwner
from .serializers import CustomerDetailSerializer, AddressSerializer, PaymentSerializer


###
# Profile
###
class UpdateDetailCustomerAPIView(generics.RetrieveUpdateAPIView):
    """
    Update detail customer profile API view.
    Only customer can access his data and update it.
    """
    permission_classes = [IsCustomer]
    queryset = Customer.objects.all()
    serializer_class =CustomerDetailSerializer
    
    def get_object(self, *args, **kwargs):
        # get current customer user.
        obj = get_object_or_404(Customer, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


###
# Address
###
class AddressListAPIView(generics.ListAPIView):
    """Customer Address list API view."""
    permission_classes = [IsCustomer]
    serializer_class = AddressSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the addresses
        for the currently authenticated customer.
        """
        return Address.objects.filter(customer=self.request.user.customer)


class AddressCreateAPIView(generics.CreateAPIView):
    """
    Customer Address create API view.
    Only a customer can create it.
    """
    permission_classes = [IsCustomer]
    serializer_class = AddressSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the addresses
        for the currently authenticated customer.
        """
        return Address.objects.filter(customer=self.request.user.customer)    

    def perform_create(self, serializer):
        """
        Set authenticated customer to be the address's customer automatically.
        """
        serializer.save(customer=self.request.user.customer)


class AddressUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Customer Address update delete API view.
    Only the authenticated customer can update or delete it.
    """
    permission_classes = [IsCustomerOwner]
    serializer_class = AddressSerializer

    def get_object(self, *args, **kwargs):
        # get address uuid4 from the requested url.
        address_uuid4 = self.kwargs.get("address_uuid", None)
        customer = self.request.user.customer
        obj = get_object_or_404(Address, uuid4=address_uuid4, customer=customer)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the addresses
        for the currently authenticated customer.
        """
        return Address.objects.filter(customer=self.request.user.customer)  


###
# Payment
###
class PaymentListAPIView(generics.ListAPIView):
    """Customer Payment list API view."""
    permission_classes = [IsCustomer]
    serializer_class = PaymentSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the payments
        for the currently authenticated customer.
        """
        return Payment.objects.filter(customer=self.request.user.customer)


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Customer Payment create API view.
    Only a customer can create it.
    """
    permission_classes = [IsCustomer]
    serializer_class = PaymentSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the payments
        for the currently authenticated customer.
        """
        return Payment.objects.filter(customer=self.request.user.customer)    

    def perform_create(self, serializer):
        """
        Set authenticated customer to be the payment's customer automatically.
        """
        serializer.save(customer=self.request.user.customer)


class PaymentUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Customer Payment update delete API view.
    Only the authenticated customer can update or delete it.
    """
    permission_classes = [IsCustomerOwner]
    serializer_class = PaymentSerializer

    def get_object(self, *args, **kwargs):
        # get payment uuid4 from the requested url.
        payment_uuid4 = self.kwargs.get("payment_uuid", None)
        customer = self.request.user.customer
        obj = get_object_or_404(Payment, uuid4=payment_uuid4, customer=customer)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the payments
        for the currently authenticated customer.
        """
        return Payment.objects.filter(customer=self.request.user.customer)


###
# Wishlist
###
class WishlistProductListAPIView(generics.ListAPIView):
    """Customer Wishlist Product list API view."""
    permission_classes = [IsCustomer]
    serializer_class = WishlistProductListSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the wishlist products
        for the currently authenticated customer.
        """
        return Wishlist.objects.filter(customer=self.request.user.customer)       