from django.dispatch import receiver
from django.db.models.signals import pre_save

from product.utils import unique_slug_generator
from .models import Product, ProductVariant

    
@receiver(pre_save, sender=Product)
def create_product_slug(sender, instance, *args, **kwargs):
    """Create a slug for a product before saving."""
    instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Product)
def add_product_discount_price(sender, instance, *args, **kwargs):
    """Set discount price to be equal max price if discount price is not given before saving."""
    if not instance.discount_price:
        instance.discount_price = instance.max_price


@receiver(pre_save, sender=ProductVariant)
def add_product_variant_discount_price(sender, instance, *args, **kwargs):
    """Set discount price to be equal max price if discount price is not given before saving."""
    if not instance.discount_price:
        instance.discount_price = instance.max_price