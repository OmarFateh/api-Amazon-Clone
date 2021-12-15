from django.dispatch import receiver
from django.db.models.signals import pre_save

from product.utils import unique_slug_generator
from .models import Product


@receiver(pre_save, sender=Product)
def create_product_slug(sender, instance, *args, **kwargs):
    """Create a slug for a product before saving."""
    instance.slug = unique_slug_generator(instance)