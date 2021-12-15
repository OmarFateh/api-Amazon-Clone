import factory

from merchant.models import Merchant
from accounts.models import User
# from accounts.tests.factories import MerchantUserFactory


class MerchantUserFactory(factory.django.DjangoModelFactory):
    """Create new merchant user instance."""
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail1@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'M'
    is_verified = True


class MerchantFactory(factory.django.DjangoModelFactory):
    """Create new merchant instance."""
    class Meta:
        model = Merchant
        django_get_or_create = ('user',)

    user = factory.SubFactory(MerchantUserFactory)
    company_name = 'amazon'
    gst_detail = 'detail'