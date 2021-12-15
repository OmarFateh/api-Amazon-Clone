import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import CustomerUserFactory, MerchantUserFactory, AdminUserFactory
from customer.tests.factories import CustomerFactory
from category.tests.factories import ParentCategoryFactory
from merchant.tests.factories import MerchantFactory
from .factories import (ProductFactory, AttributeFactory, AttributeValueFactory, ProductVariantFactory,
                        QuestionFactory, AnswerFactory, ReviewFactory, WishlistFactory)

register(CustomerUserFactory)
register(MerchantUserFactory)
register(AdminUserFactory)
register(CustomerFactory)
register(MerchantFactory)
register(ParentCategoryFactory)
register(ProductFactory)
register(AttributeFactory)
register(AttributeValueFactory)
register(ProductVariantFactory)
register(QuestionFactory)
register(AnswerFactory)
register(ReviewFactory)
register(WishlistFactory)


@pytest.fixture
def new_customer_user(db, customer_user_factory):
    customer = customer_user_factory.create()
    return customer


@pytest.fixture
def new_customer(db, customer_factory):
    customer = customer_factory.create()
    return customer


@pytest.fixture
def new_merchant_user(db, merchant_user_factory):
    merchant = merchant_user_factory.create()
    return merchant


@pytest.fixture
def new_merchant(db, merchant_factory):
    merchant = merchant_factory.create()
    return merchant


@pytest.fixture
def new_admin_user(db, admin_user_factory):
    admin = admin_user_factory.create()
    return admin


@pytest.fixture
def new_parent_category(db, parent_category_factory):
    category = parent_category_factory.create()
    return category


@pytest.fixture
def new_product(db, product_factory):
    product = product_factory.create()
    return product


@pytest.fixture
def new_attribute(db, attribute_factory):
    attribute = attribute_factory.create()
    return attribute


@pytest.fixture
def new_attribute_value(db, attribute_value_factory):
    attribute_value = attribute_value_factory.create()
    return attribute_value


@pytest.fixture
def new_product_variant(db, product_variant_factory):
    product_variant = product_variant_factory.create()
    return product_variant


@pytest.fixture
def new_question(db, question_factory):
    question = question_factory.create()
    return question


@pytest.fixture
def new_answer(db, answer_factory):
    answer = answer_factory.create()
    return answer


@pytest.fixture
def new_review(db, review_factory):
    review = review_factory.create()
    return review


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