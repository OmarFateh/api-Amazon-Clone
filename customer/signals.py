from django.dispatch import receiver
from django.db.models.signals import pre_save

from product.utils import unique_slug_generator
from .models import Address, Payment


@receiver(pre_save, sender=Address)
def update_address_default(sender, instance, *args, **kwargs):
    """
    Set all other addresses to be not default if the instance is a default.
    """
    if instance.is_default:
        Address.objects.update(is_default=False)


@receiver(pre_save, sender=Payment)
def update_payment_default(sender, instance, *args, **kwargs):
    """
    Set all other payments to be not default if the instance is a default.
    """
    if instance.is_default:
        Payment.objects.update(is_default=False)