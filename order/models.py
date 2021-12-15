from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from useradmin.models import BaseTimestamp
from customer.models import Customer, Address, Payment
from product.models import ProductVariant


class Order(BaseTimestamp):
    """Order model"""
    BILLING_STATUS = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )
    SHIPPING_STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name='orders', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    billing_status = models.CharField(max_length=6, choices=BILLING_STATUS, default='Unpaid')
    shipping_status = models.CharField(max_length=9, choices=SHIPPING_STATUS, default='Pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return cutomer's email, total paid, billing status, shipping status.
        return f"{self.customer.user.email} | {self.total_paid} | {self.billing_status} | {self.shipping_status}"


class OrderItem(BaseTimestamp):
    """Order item model"""
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return product variant, purchase price, quantity.
        return f"{self.product_variant} | {self.purchase_price} | {self.quantity}"


class Coupon(BaseTimestamp):
    """Coupon model"""
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    # discount_amount = models.PositiveIntegerField(default=1)
    discount_amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # Return coupon's code.
        return self.code