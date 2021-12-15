import json
import os

from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from category.models import Category


class TestCategory:

    category_list_endpoint = reverse('category-api:list')
    category_create_endpoint = reverse('category-api:create')
    category_detail_endpoint = reverse(
        'category-api:detail', kwargs={"category_slug": 'test-parent-category'})
    category_update_delete_endpoint = reverse(
        'category-api:update-delete', kwargs={"category_slug": 'test-parent-category'})
    upload_file = open(os.path.join(settings.BASE_DIR,
                                    'static/img/no_avatar.jpg'), "rb")
    thumbnail = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    data = {'title': 'test', 'thumbnail': thumbnail, 'description': 'test category', 'parent_id': 1}
    
    def test_category_list(self, db, new_parent_category, api_client):
        """
        Test category retrieve list response status.
        """
        response = api_client.get(self.category_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_category_create(self, db, new_admin, new_parent_category, api_client):
        """
        Test category create response status.
        """
        api_client.force_authenticate(new_admin)
        assert Category.objects.count() == 1
        response = api_client.post(
            self.category_create_endpoint, self.data, format='multipart')
        assert response.status_code == 201
        assert Category.objects.count() == 2

    def test_category_detail(self, db, new_parent_category, api_client):
        """
        Test category detail response status.
        """
        response = api_client.get(self.category_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_category_update(self, db, new_admin, new_parent_category, api_client):
        """
        Test category update response status.
        """
        api_client.force_authenticate(new_admin)
        assert new_parent_category.title == 'test parent category'
        data = {'title': 'test'}
        response = api_client.patch(
            self.category_update_delete_endpoint, data)
        new_parent_category.refresh_from_db()
        assert response.status_code == 200
        assert new_parent_category.title == 'Test'

    def test_category_delete(self, db, new_admin, new_parent_category, api_client):
        """
        Test category delete response status.
        """
        api_client.force_authenticate(new_admin)
        assert Category.objects.count() == 1
        response = api_client.delete(self.category_update_delete_endpoint)
        assert response.status_code == 204
        assert Category.objects.count() == 0 