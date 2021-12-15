import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import AdminUserFactory
from .factories import ParentCategoryFactory, CategoryFactory

register(ParentCategoryFactory)
register(CategoryFactory)
register(AdminUserFactory)


@pytest.fixture
def new_parent_category(db, parent_category_factory):
    category = parent_category_factory.create()
    return category


@pytest.fixture
def new_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def new_admin(db, admin_user_factory):
    admin = admin_user_factory.create()
    return admin


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def api_factory():
    return APIRequestFactory()