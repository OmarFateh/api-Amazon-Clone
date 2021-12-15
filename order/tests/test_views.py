import json

from django.urls import reverse

from order.models import Order, OrderItem, Coupon


class TestOrder:
    
    list_create_endpoint = reverse('order-api:orders-list-create')
    update_delete_endpoint = reverse('order-api:orders-update-delete',
                                        kwargs={"order_id": 1})
    data = {'customer': 1, 'shipping_address': 1, 'payment': 1, 'coupon': 1, 'total_paid': 500, 
            'order_items':[{'product_variant': 1, "purchase_price": 500, "discount_amount": 100, "quantity": 3}]}

    def test_order_list(self, db, new_customer_user, new_order, api_client):
        """Test order retrieve list response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.list_create_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_order_create(self, db, new_customer_user, new_customer, new_shipping_address, new_payment, new_coupon, api_client):
        """Test order create response status."""
        api_client.force_authenticate(new_customer_user)
        assert Order.objects.count() == 0
        response = api_client.post(self.list_create_endpoint, self.data)
        assert response.status_code == 201
        assert Order.objects.count() == 1

    def test_order_detail(self, db, new_customer_user, new_order, api_client):
        """Test order detail response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.update_delete_endpoint, format='json')
        assert response.status_code == 200

    def test_order_update(self, db, new_customer_user, new_order, api_client):
        """Test order update response status."""
        api_client.force_authenticate(new_customer_user)
        assert new_order.total_paid == 500
        data = {'total_paid': 800}
        response = api_client.patch(self.update_delete_endpoint, data)
        new_order.refresh_from_db()
        assert response.status_code == 200
        assert new_order.total_paid == 800

    def test_order_delete(self, db, new_customer_user, new_order, api_client):
        """Test order delete response status."""
        api_client.force_authenticate(new_customer_user)
        assert Order.objects.count() == 1
        response = api_client.delete(self.update_delete_endpoint)
        assert response.status_code == 204
        assert Order.objects.count() == 0


class TestCoupon:

    list_create_endpoint = reverse('order-api:coupons-list-create')
    update_delete_endpoint = reverse('order-api:coupons-update-delete',
                                        kwargs={"coupon_id": 1})
    data = {'code': 'test code', 'valid_from': '2021-02-01', 'valid_to': '2021-03-03', 'discount_amount': 10, 'is_active': True}

    def test_coupon_list(self, db, new_admin_user, new_coupon, api_client):
        """Test coupon retrieve list response status."""
        api_client.force_authenticate(new_admin_user)
        response = api_client.get(self.list_create_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_coupon_create(self, db, new_admin_user, api_client):
        """Test coupon create response status."""
        api_client.force_authenticate(new_admin_user)
        assert Coupon.objects.count() == 0
        response = api_client.post(self.list_create_endpoint, self.data)
        assert response.status_code == 201
        assert Coupon.objects.count() == 1

    def test_coupon_detail(self, db, new_admin_user, new_coupon, api_client):
        """Test coupon detail response status."""
        api_client.force_authenticate(new_admin_user)
        response = api_client.get(self.update_delete_endpoint, format='json')
        assert response.status_code == 200

    def test_coupon_update(self, db, new_admin_user, new_coupon, api_client):
        """Test coupon update response status."""
        api_client.force_authenticate(new_admin_user)
        assert new_coupon.discount_amount == 10
        data = {'discount_amount': 20}
        response = api_client.patch(self.update_delete_endpoint, data)
        new_coupon.refresh_from_db()
        assert response.status_code == 200
        assert new_coupon.discount_amount == 20

    def test_coupon_delete(self, db, new_admin_user, new_coupon, api_client):
        """Test coupon delete response status."""
        api_client.force_authenticate(new_admin_user)
        assert Coupon.objects.count() == 1
        response = api_client.delete(self.update_delete_endpoint)
        assert response.status_code == 204
        assert Coupon.objects.count() == 0