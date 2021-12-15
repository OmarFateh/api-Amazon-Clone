import factory

from customer.models import Customer, Address, Payment
from accounts.tests.factories import CustomerUserFactory


class CustomerFactory(factory.django.DjangoModelFactory):
    """Create new customer instance."""
    class Meta:
        model = Customer
        django_get_or_create = ('user',)

    user = factory.SubFactory(CustomerUserFactory)


class AddressFactory(factory.django.DjangoModelFactory):
    """Create new address instance."""
    class Meta:
        model = Address
        django_get_or_create = ('uuid4',)

    customer = factory.SubFactory(CustomerFactory)
    uuid4 = "36e6abc3-6c46-4624-8e29-52340ceaf53b"
    full_name = 'Dr. Nettie Kovacek'
    phone = '764-502-4487'
    address_line1 = '17013 West Summit'
    address_line2 = '753 Marielle Loop'
    country = 'Guadeloupe'
    city = 'West Thomastown'
    postal_code = '55202'
    is_default = False


class PaymentFactory(factory.django.DjangoModelFactory):
    """Create new payment instance."""
    class Meta:
        model = Payment
        django_get_or_create = ('uuid4',)

    customer = factory.SubFactory(CustomerFactory)
    uuid4 = "36e6abc3-6c46-4624-8e29-52340ceaf53b"
    payment_type = 'PayPal'
    provider = 'Bank Misr'
    account_no = '24-774-671-6055'
    expiry_date = '2020-03-10'
    is_default = False