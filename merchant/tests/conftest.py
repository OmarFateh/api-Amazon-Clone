import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

# from accounts.tests.factories import MerchantUserFactory
from .factories import MerchantFactory, MerchantUserFactory

register(MerchantFactory)
register(MerchantUserFactory)


@pytest.fixture
def new_merchant(db, merchant_factory):
    merchant = merchant_factory.create()
    return merchant


@pytest.fixture
def new_merchant_user(db, merchant_user_factory):
    merchant = merchant_user_factory.create()
    return merchant


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()