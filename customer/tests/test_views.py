import json

from django.urls import reverse

from customer.models import Address, Payment


class TestUpdateDetailPatient:
    
    data = {'first_name': 'test name'}
    url = reverse('customer-api:customer-profile-detail-update')

    def test_customer_detail(self, db, new_customer_user, api_client):
        """Test customer detail response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.url, format='json')
        assert response.status_code == 200

    def test_customer_update(self, db, new_customer_user, api_client):
        """Test customer update response status."""
        api_client.force_authenticate(new_customer_user)
        assert new_customer_user.first_name == 'omar'
        response = api_client.patch(self.url, self.data)
        new_customer_user.refresh_from_db()
        assert response.status_code == 200
        assert new_customer_user.first_name == 'test name'


class TestAddress:

    address_list_endpoint = reverse('customer-api:address-list')
    address_create_endpoint = reverse('customer-api:address-create')
    address_detail_endpoint = reverse(
        'customer-api:address-detail', kwargs={"address_uuid": '36e6abc3-6c46-4624-8e29-52340ceaf53b'})
    data = {'full_name': 'test name', 'phone': '775-522-584-215', 'address_line1': 'giza',
        'address_line2': 'giza', 'country': 'Egypt', 'city': 'cairo', 
        'postal_code': '55241', 'is_default': False}
    
    def test_address_list(self, db, new_customer_user, new_address, api_client):
        """Test address retrieve list response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.address_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_address_create(self, db, new_customer_user, api_client):
        """Test address create response status."""
        api_client.force_authenticate(new_customer_user)
        assert Address.objects.count() == 0
        response = api_client.post(self.address_create_endpoint, self.data)
        assert response.status_code == 201
        assert Address.objects.count() == 1

    def test_address_detail(self, db, new_customer_user, new_address, api_client):
        """Test address detail response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.address_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_address_update(self, db, new_customer_user, new_address, api_client):
        """Test address update response status."""
        api_client.force_authenticate(new_customer_user)
        assert new_address.full_name == 'Dr. Nettie Kovacek'
        data = {'full_name': 'test full name'}
        response = api_client.patch(self.address_detail_endpoint, data)
        new_address.refresh_from_db()
        assert response.status_code == 200
        assert new_address.full_name == 'test full name'

    def test_address_delete(self, db, new_customer_user, new_address, api_client):
        """Test address delete response status."""
        api_client.force_authenticate(new_customer_user)
        assert Address.objects.count() == 1
        response = api_client.delete(self.address_detail_endpoint)
        assert response.status_code == 204
        assert Address.objects.count() == 0 


class TestPayment:
    
    payment_list_endpoint = reverse('customer-api:payment-list')
    payment_create_endpoint = reverse('customer-api:payment-create')
    payment_detail_endpoint = reverse(
        'customer-api:payment-detail', kwargs={"payment_uuid": '36e6abc3-6c46-4624-8e29-52340ceaf53b'})
    data = {'payment_type': 'PayPal', 'provider': 'Bank', 'account_no': '24-774-671-6055',
            'expiry_date': '2020-03-10', 'is_default': False}
    
    def test_payment_list(self, db, new_customer_user, new_payment, api_client):
        """Test payment retrieve list response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.payment_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_payment_create(self, db, new_customer_user, api_client):
        """Test payment create response status."""
        api_client.force_authenticate(new_customer_user)
        assert Payment.objects.count() == 0
        response = api_client.post(self.payment_create_endpoint, self.data)
        assert response.status_code == 201
        assert Payment.objects.count() == 1

    def test_payment_detail(self, db, new_customer_user, new_payment, api_client):
        """Test payment detail response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.payment_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_payment_update(self, db, new_customer_user, new_payment, api_client):
        """Test payment update response status."""
        api_client.force_authenticate(new_customer_user)
        assert new_payment.payment_type == 'PayPal'
        data = {'payment_type': 'Stripe'}
        response = api_client.patch(self.payment_detail_endpoint, data)
        new_payment.refresh_from_db()
        assert response.status_code == 200
        assert new_payment.payment_type == 'Stripe'

    def test_payment_delete(self, db, new_customer_user, new_payment, api_client):
        """Test payment delete response status."""
        api_client.force_authenticate(new_customer_user)
        assert Payment.objects.count() == 1
        response = api_client.delete(self.payment_detail_endpoint)
        assert response.status_code == 204
        assert Payment.objects.count() == 0


class TestWishlist:
    
    wishlist_list_endpoint = reverse('customer-api:wishlist-list')
    
    def test_wishlist_list(self, db, new_customer_user, new_wishlist, api_client):
        """Test wishlist products retrieve list response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.wishlist_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1