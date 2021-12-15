from order.serializers import OrderItemSerializer, OrderSerializer, CouponSerializer


class TestOrderItemSerializer:
    
    data = {'product_variant': 1, "purchase_price": 500, "discount_amount": 100, "quantity": 3, 'item_id': 1}

    def test_create_valid_serializer(self, db, new_product_variant):
        """Test valid create order item serializer data."""
        serializer = OrderItemSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestOrderSerializer:

    data = {'customer': 1, 'shipping_address': 1, 'payment': 1, 'coupon': 1, 'total_paid': 500, 
            'order_items':[{'product_variant': 1, "purchase_price": 500, "discount_amount": 100, "quantity": 3, 'item_id': 1}]}

    def test_create_valid_serializer(self, db, new_customer, new_shipping_address, new_payment, new_coupon, new_product_variant):
        """Test valid create order serializer data."""
        serializer = OrderSerializer(data=self.data, context={'is_update': False})
        assert serializer.is_valid() == True

    def test_update_wrong_item_id(self, db, new_order):
        """Test item id is not in order's items in update view."""
        self.data["order_items"] = [{"item_id": 5, "quantity": 5}]
        serializer = OrderSerializer(data=self.data, instance=new_order, partial=True,
                        context={'is_update': True, "order_obj": new_order})
        assert serializer.is_valid() == False
        assert serializer.errors['order_items']['item_id'] == "This order does not have this item id."

    def test_update_fields_required(self, db, new_order, new_product_variant):
        """Test required fields are not given while item id in not given in update view."""
        self.data["order_items"] = [{"product_variant": 1, "quantity": 5}]
        serializer = OrderSerializer(data=self.data, instance=new_order, partial=True,
                        context={'is_update': True, "order_obj": new_order})
        assert serializer.is_valid() == False
        assert serializer.errors['order_items']['purchase_price'] == 'This field is required.'
            

class TestCouponSerializer:

    data = {'code': 'test code', 'valid_from': '2021-02-01', 'valid_to': '2021-03-03', 'discount_amount': 10, 'is_active': True}

    def test_create_valid_serializer(self, db):
        """Test valid create coupon serializer data."""
        serializer = CouponSerializer(data=self.data)
        assert serializer.is_valid() == True

    def test_create_coupon_already_exists(self, db, new_coupon):
        """Test coupon already exists in create view."""
        serializer = CouponSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['code'][0] == 'coupon with this code already exists.'

    def test_update_coupon_already_exists(self, db, new_coupon):
        """Test coupon already exists in update view."""
        serializer = CouponSerializer(data=self.data, instance=new_coupon)
        assert serializer.is_valid() == True

    def test_create_valid_from_greater_valid_to_dates(self, db):
        """Test valid from date greater than valid to date in create view."""
        self.data['valid_from'] = '2021-04-04'
        serializer = CouponSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['valid_from'][0] == 'Valid from date should be earlier than valid to date.'   