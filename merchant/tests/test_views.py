import json

from django.urls import reverse

from merchant.models import Merchant


class TestUpdateDetailMerchant:
    
    data = {'first_name': 'test name', 'company_name': 'microsoft'}
    url = reverse('merchant-api:merchant-profile-detail-update')

    def test_merchant_detail(self, db, new_merchant_user, api_client):
        """Test merchant detail response status."""
        api_client.force_authenticate(new_merchant_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200

    def test_merchant_update(self, db, new_merchant_user, new_merchant, api_client):
        """Test merchant update response status."""
        api_client.force_authenticate(new_merchant_user)
        assert new_merchant_user.first_name == 'omar'
        assert new_merchant.company_name == 'amazon'
        response = api_client.patch(self.url, self.data, format='json')
        new_merchant_user.refresh_from_db()
        assert response.status_code == 200
        assert new_merchant_user.first_name == 'test name'
        assert new_merchant.company_name == 'microsoft'