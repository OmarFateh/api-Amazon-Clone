import os

from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from category.serializers import CategorySerializer


class TestCategorySerializer:
    
    category_create_endpoint = reverse('category-api:create')
    category_update_delete_endpoint = reverse(
        'category-api:update-delete', kwargs={"category_slug": 'test-parent-category'})
    upload_file = open(os.path.join(settings.BASE_DIR,
                                    'static/img/no_avatar.jpg'), "rb")
    thumbnail = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    data = {'title': 'test category', 'thumbnail': thumbnail, 'description': 'test category', 'parent_id': 2}

    def test_valid_serializer(self, db):
        """Test valid category serializer data."""
        serializer = CategorySerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == True

    def test_invalid_parent_id_value(self, db):
        """Test invalid parent id value data."""
        self.data['parent_id'] = 'str'
        serializer = CategorySerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == False
        assert serializer.errors['parent_id'][0] == 'You must supply an integer'

    def test_none_parent_id_value(self, db):
        """Test none parent id value data."""
        self.data['parent_id'] = None
        serializer = CategorySerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == True  

    def test_create_category_already_exists(self, db, new_parent_category, new_category):
        """Test a parent category can't have the same child category twice."""
        self.data['title'] = 'test category'
        self.data['parent_id'] = 1
        serializer = CategorySerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == False
        assert serializer.errors['non_field_errors'][0] == 'This category already exists with this parent category'      

    def test_update_category_already_exists(self, db, new_parent_category, new_category):
        """Test a parent category can't have the same child category twice."""
        self.data['title'] = 'test category'
        self.data['parent_id'] = 1
        serializer = CategorySerializer(data=self.data, context={'category': new_category, 'is_create': False})
        assert serializer.is_valid() == True