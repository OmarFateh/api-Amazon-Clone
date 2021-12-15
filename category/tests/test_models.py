import os

from django.conf import settings

import pytest

from category.models import Category


class TestModel:

    def test_category_str(self, new_category):
        """
        Test category obj str method.
        """
        assert new_category.__str__() == 'test category'
    
    def test_get_parent(self, new_category, new_parent_category):
        """
        Test get category parent obj method.
        """
        # has parent 
        assert new_category.get_parent() == new_parent_category
        # has no parent
        assert new_parent_category.get_parent() == new_parent_category

    def test_category_thumbnail_upload_path(self, new_category):
        """
        Test upload path of category thumbnail.
        """
        photo_name = new_category.thumbnail.name.split('/')[-1]
        photo_path = os.path.join(
            settings.BASE_DIR, f'media\\categories\\test category\\{photo_name}')
        assert new_category.thumbnail.path == photo_path