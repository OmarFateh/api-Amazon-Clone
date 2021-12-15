from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

from useradmin.models import BaseTimestamp
from .fields import TitleCharField


def category_thumbnail(instance, filename):
    """Upload the category image into the path and return the uploaded image path."""   
    return f'categories/{instance.name}/{filename}'


class Category(MPTTModel, BaseTimestamp):
    """Category model implemented with MPTT."""
    name = TitleCharField(max_length=64, title=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=category_thumbnail)
    description = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'parent')
        verbose_name_plural = 'Categories'

    def __str__(self):
        # Return category's name
        return self.name

    def get_parent(self):
        # Return category's parent. 
        if self.parent:
            return self.parent 
        else: 
            return self     