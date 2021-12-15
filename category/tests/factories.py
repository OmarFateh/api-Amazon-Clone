import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

import factory

from category.models import Category

upload_file = open(os.path.join(settings.BASE_DIR,
                                'static/img/no_avatar.jpg'), "rb")


class ParentCategoryFactory(factory.django.DjangoModelFactory):
    """Create new parent category instance."""
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = 'test parent category'
    slug = 'test-parent-category'
    thumbnail = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    description = 'test parent category'


class CategoryFactory(factory.django.DjangoModelFactory):
    """Create new category instance."""
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = 'test category'
    slug = 'test-parent-category/test-category'
    thumbnail = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    description = 'test category'
    parent = factory.SubFactory(ParentCategoryFactory)