import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import CustomerUserFactory, AdminUserFactory
from customer.tests.factories import CustomerFactory, AddressFactory, PaymentFactory
from product.tests.factories import ProductVariantFactory
from .factories import CouponFactory, OrderFactory, OrderItemFactory

register(CouponFactory)
register(OrderFactory)
register(OrderItemFactory)
register(AdminUserFactory)
register(CustomerUserFactory)
register(CustomerFactory)
register(AddressFactory)
register(PaymentFactory)
register(ProductVariantFactory)


@pytest.fixture
def new_coupon(db, coupon_factory):
    coupon = coupon_factory.create()
    return coupon


@pytest.fixture
def new_order(db, order_factory):
    order = order_factory.create()
    return order


@pytest.fixture
def new_order_item(db, order_item_factory):
    order_item = order_item_factory.create()
    return order_item


@pytest.fixture
def new_admin_user(db, admin_user_factory):
    admin = admin_user_factory.create()
    return admin


@pytest.fixture
def new_customer_user(db, customer_user_factory):
    customer = customer_user_factory.create()
    return customer


@pytest.fixture
def new_customer(db, customer_factory):
    customer = customer_factory.create()
    return customer


@pytest.fixture
def new_shipping_address(db, address_factory):
    address = address_factory.create()
    return address


@pytest.fixture
def new_payment(db, payment_factory):
    payment = payment_factory.create()
    return payment


@pytest.fixture
def new_product_variant(db, product_variant_factory):
    product_variant = product_variant_factory.create()
    return product_variant


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()