from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from useradmin.models import BaseTimestamp
from customer.models import Customer
from merchant.models import Merchant
from category.models import Category
from category.fields import TitleCharField


def product_variant_image(instance, filename):
    """Upload the product variant image into the path and return the uploaded image path."""   
    return f'products/{instance.variant.product.category}/{instance.variant.product}/{filename}'


class ProductCommonData(BaseTimestamp):
    """Product common data abstract model to be inherited from."""
    total_in_stock = models.PositiveIntegerField()
    is_in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Attribute(BaseTimestamp):
    """attribute can be like color, material, size, shape....etc"""
    name = TitleCharField(max_length=64, unique=True, title=True)

    def __str__(self):
        # Return attribute name
        return self.name


class AttributeValue(BaseTimestamp):
    """
    Values for the selected attribute like for size attr
    the values can be Large, Medium, Small....etc
    """
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    name = TitleCharField(max_length=64, title=True)

    class Meta:
        unique_together = ('attribute', 'name')

    def __str__(self):
        # Return attribute name & attribute value name
        return f"{self.attribute.name} | {self.name}"


class ProductManager(models.Manager):
    """Product model manager."""
    def get_descendants_products(self, category, ids=None):
        """
        Take category, and get all products of descendants categories of this category.
        If ids is given, get all products ids of descendants categories of this category.
        """
        if ids:
            return self.get_queryset().filter(category__in=category.get_descendants(
                                            include_self=True)).values_list('id', flat=True).distinct()
        else:
            return self.get_queryset().filter(category__in=category.get_descendants(include_self=True)) 


class Product(ProductCommonData):
    """Product model."""
    merchant = models.ForeignKey(Merchant, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.CharField(max_length=255)
    details = models.TextField()

    objects = ProductManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return product's name.
        return f"{self.name}"


class ProductVariant(ProductCommonData):
    """This model holds the values for price and combination of attributes for a product."""
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant =  models.ManyToManyField(AttributeValue)
        
    def __str__(self):
        # Return product's name
        return f"{self.product}"

    @property
    def merchant(self):
        # Return product's merchant 
        return self.product.merchant

    @property
    def actual_price(self):
        # Return discount price if exists and if not, get max price. 
        if self.discount_price:
            return self.discount_price
        else:
            return self.max_price

    @property
    def get_price_discount_difference(self):
        # Return the difference between max price and discount price.
        if self.discount_price:
            return self.max_price - self.discount_price

    @property
    def get_price_discount_difference_percentage(self):
        # Return the percentage difference between max price and discount price.
        if self.discount_price:
            return (self.get_price_discount_difference*100) // self.max_price


class ProductVariantImage(BaseTimestamp):
    """Product image model."""
    variant = models.ForeignKey(ProductVariant, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_variant_image)
    is_thumbnail = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # objects = ProductImageManager()

    class Meta:
        ordering = ['variant']

    def __str__(self):
        # Return product's variant.
        return f"{self.variant}"

    @property
    def merchant(self):
        # Return product's merchant 
        return self.variant.product.merchant


class Question(BaseTimestamp):
    """Product Question model."""
    product = models.ForeignKey(Product, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.user", related_name='questions', on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # Return product's name and user's email.
        return f"{self.product.name} | {self.user.email}"


class Answer(BaseTimestamp):
    """Product Question Answer model."""
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.user", related_name='answers', on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # Return question product's name and user's email.
        return f"{self.question.product.name} | {self.user.email}"


class Review(BaseTimestamp):
    """Product Review model."""
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey("customer.customer", related_name='reviews', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.TextField()
    rate = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['product', 'customer']
        ordering = ['-created_at']

    def __str__(self):
        # Return Product's name, user's email and his rate.
        return f"{self.product.name} | {self.customer.user.email} | {self.rate} stars"

    @property
    def get_rate_percentage(self):
        # Return review rate percentage.
        return (self.rate * 20)


class Wishlist(BaseTimestamp):
    """Customer Product Wishlist model."""
    customer = models.ForeignKey("customer.customer", related_name='wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['product', 'customer']

    def __str__ (self):
        # Return customer's email & product's name.
        return f'{self.customer.user.email} | {self.product}'
