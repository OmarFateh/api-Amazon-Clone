import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import AdminUserFactory
from .factories import AdminFactory

register(AdminFactory)
register(AdminUserFactory)


@pytest.fixture
def new_admin_user(db, admin_user_factory):
    admin = admin_user_factory.create()
    return admin


@pytest.fixture
def new_admin(db, admin_factory):
    admin = admin_factory.create()
    return admin


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()