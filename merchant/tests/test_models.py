import pytest


class TestMerchantModel:
    
    def test_merchant_str(self, new_merchant_user, new_merchant):
        """Test merchant obj str method."""
        print('company', new_merchant_user.merchant.company_name)
        assert new_merchant.company_name == 'amazon'
        assert new_merchant.__str__() == 'testemail1@gmail.com | '