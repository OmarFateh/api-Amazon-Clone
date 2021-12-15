import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import CustomerUserFactory
from product.tests.factories import WishlistFactory
from .factories import CustomerFactory, AddressFactory, PaymentFactory

register(CustomerFactory)
register(CustomerUserFactory)
register(AddressFactory)
register(PaymentFactory)
register(WishlistFactory)


@pytest.fixture
def new_customer(db, customer_factory):
    customer = customer_factory.create()
    return customer


@pytest.fixture
def new_customer_user(db, customer_user_factory):
    customer = customer_user_factory.create()
    return customer


@pytest.fixture
def new_address(db, address_factory):
    address = address_factory.create()
    return address


@pytest.fixture
def new_payment(db, payment_factory):
    payment = payment_factory.create()
    return payment


@pytest.fixture
def new_wishlist(db, wishlist_factory):
    wishlist = wishlist_factory.create()
    return wishlist

    
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()