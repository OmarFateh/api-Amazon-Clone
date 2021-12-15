import uuid

from django.db import models

from useradmin.models import BaseTimestamp


class Customer(BaseTimestamp):
    """Customer model with one to one relation with custom user model."""
    user = models.OneToOneField("accounts.user", related_name='customer' , on_delete=models.CASCADE)

    def __str__ (self):
        # Return customer's email.
        return self.user.email


class Address(BaseTimestamp):
    """Customer Address model."""
    uuid4 = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=16)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=16)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-is_default']

    def __str__ (self):
        # Return customer's full name & email.
        return f'{self.full_name} | {self.customer.user.email}'


class Payment(BaseTimestamp):
    """Customer Payment model."""
    TYPES_CHOICES = (
        ('Stripe', 'Stripe'),
        ('PayPal', 'PayPal'),
    )

    uuid4 = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, related_name='payments', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=6, choices=TYPES_CHOICES, default='PayPal')
    provider = models.CharField(max_length=255)
    account_no = models.CharField(max_length=255)
    expiry_date = models.DateField()
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_default']

    def __str__ (self):
        # Return customer's email & payment type.
        return f'{self.customer.user.email} | {self.payment_type}'