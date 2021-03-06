from django.dispatch import receiver
from django.db.models.signals import pre_save

from product.utils import unique_slug_generator
from .models import Brand


@receiver(pre_save, sender=Brand)
def create_brand_slug(sender, instance, *args, **kwargs):
    """Create a slug for a brand before saving."""
    instance.slug = unique_slug_generator(instance)