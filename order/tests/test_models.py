import pytest

from order.models import Coupon


class TestOrderModel:
    
    def test_order_str(self, new_order):
        """Test order obj str method."""
        assert new_order.__str__() == 'testemail@gmail.com | 500 | Unpaid | Pending'


class TestOrderItemModel:
    
    def test_order_item_str(self, new_order_item):
        """Test order item obj str method."""
        assert new_order_item.__str__() == 'test title | 900 | 3'


class TestCouponModel:

    def test_coupon_str(self, new_coupon):
        """Test coupon obj str method."""
        assert new_coupon.__str__() == 'test code'