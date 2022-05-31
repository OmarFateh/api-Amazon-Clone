from django.db import models

from useradmin.models import BaseTimestamp
from category.fields import TitleCharField


def brand_thumbnail(instance, filename):
    """Upload the brand image into the path and return the uploaded image path."""   
    return f'brands/{instance.name}/{filename}'


class Brand(BaseTimestamp):
    """Brand model."""
    name = TitleCharField(max_length=64, title=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=brand_thumbnail, null=True)
    
    def __str__(self):
        # Return brand's name.
        return f"{self.name}"