import factory

from order.models import Coupon, Order, OrderItem
from customer.tests.factories import CustomerFactory, AddressFactory, PaymentFactory
from product.tests.factories import ProductVariantFactory


class CouponFactory(factory.django.DjangoModelFactory):
    """Create new coupon instance."""
    class Meta:
        model = Coupon
        django_get_or_create = ('code',)

    code = "test code"
    valid_from = "2021-02-01"
    valid_to = "2021-03-03"
    discount_amount = 10
    is_active = True


class OrderFactory(factory.django.DjangoModelFactory):
    """Create new order instance."""
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    shipping_address = factory.SubFactory(AddressFactory)
    payment = factory.SubFactory(PaymentFactory)
    coupon = factory.SubFactory(CouponFactory)
    total_paid = 500
    billing_status = "Unpaid"
    shipping_status = "Pending"


class OrderItemFactory(factory.django.DjangoModelFactory):
    """Create new order item instance."""
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    purchase_price = 900
    discount_amount = 300
    quantity = 3