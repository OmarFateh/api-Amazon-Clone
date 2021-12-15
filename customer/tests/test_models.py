import pytest


class TestCustomerModel:
    
    def test_customer_str(self, new_customer):
        """Test customer obj str method."""
        assert new_customer.__str__() == 'testemail@gmail.com'


class TestAddressModel:

    def test_address_str(self, new_address):
        """Test address obj str method."""
        assert new_address.__str__() == 'Dr. Nettie Kovacek | testemail@gmail.com'


class TestPaymentModel:
    
    def test_payment_str(self, new_payment):
        """Test payment obj str method."""
        assert new_payment.__str__() == 'testemail@gmail.com | PayPal'