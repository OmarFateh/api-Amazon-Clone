import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from .factories import CustomerUserFactory

register(CustomerUserFactory)


@pytest.fixture
def new_user(db, customer_user_factory):
    user = customer_user_factory.create()
    return user

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def api_factory():
    return APIRequestFactory()