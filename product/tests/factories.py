import factory

from merchant.models import Merchant
from product.models import Answer, Attribute, AttributeValue, Product, ProductVariant, Question, Review, Wishlist
from accounts.tests.factories import MerchantUserFactory
from category.tests.factories import ParentCategoryFactory
from customer.tests.factories import CustomerFactory
from merchant.tests.factories import MerchantFactory


class AttributeFactory(factory.django.DjangoModelFactory):
    """Create new attribute instance."""
    class Meta:
        model = Attribute
        django_get_or_create = ('name',)

    name = "test attribute"


class AttributeValueFactory(factory.django.DjangoModelFactory):
    """Create new attribute value instance."""
    class Meta:
        model = AttributeValue
        django_get_or_create = ('name', 'attribute',)

    attribute = factory.SubFactory(AttributeFactory)
    name = "test attribute value"


class ProductFactory(factory.django.DjangoModelFactory):
    """Create new product instance."""
    class Meta:
        model = Product
        django_get_or_create = ('slug',)

    merchant = factory.SubFactory(MerchantFactory)
    category = factory.SubFactory(ParentCategoryFactory)
    name = "test title"
    slug = "test-title"
    description = 'description'
    details = 'details'
    total_in_stock = 50
    is_in_stock = True
    is_active = True


class ProductVariantFactory(factory.django.DjangoModelFactory):
    """Create new product variant instance."""
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    max_price = 700
    discount_price = 500
    total_in_stock = 10
    is_in_stock = True
    is_active = True

    @factory.post_generation
    def variant(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for variant_obj in extracted:
                self.variant.add(variant_obj)


class QuestionFactory(factory.django.DjangoModelFactory):
    """Create new question instance."""
    class Meta:
        model = Question

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(MerchantUserFactory)
    content = "question content"
    is_active = True


class AnswerFactory(factory.django.DjangoModelFactory):
    """Create new answer instance."""
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    user = factory.SubFactory(MerchantUserFactory)
    content = "answer content"
    is_active = True


class ReviewFactory(factory.django.DjangoModelFactory):
    """Create new review instance."""
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    title = "review title"
    content = "review content"
    rate = 5
    is_active = True


class WishlistFactory(factory.django.DjangoModelFactory):
    """Create new product wishlist instance."""
    class Meta:
        model = Wishlist

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    is_active = True