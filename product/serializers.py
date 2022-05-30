from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce

from rest_framework import serializers

from accounts.serializers import UserSerializer
from customer.serializers import CustomerDetailSerializer
from .mixins import TimestampMixin
from .utils import compare_max_discount_price
from .models import (Product, Attribute, AttributeValue, ProductVariant, 
                        ProductVariantImage, Question, Answer, Review, Wishlist)


###
# Variant Attribute
###
class AttributeSerializer(serializers.ModelSerializer, TimestampMixin):
    """Attribute model serializer."""
    values = serializers.SerializerMethodField()
    class Meta:
        model  = Attribute
        fields = ["id", "name", "values"]

    def get_values(self, obj):
        """Return all attribute values for this attribute."""
        values = AttributeValue.objects.select_related('attribute').filter(attribute=obj)
        if values:
            return AttributeValueSerializer(values, many=True).data
        else:
            return None

    def validate_name(self, value):
        """Validate that attribute name is unique."""
        is_create = self.context['is_create']
        error = False
        if is_create:
            if Attribute.objects.filter(name__iexact=value).exists():
                error = True
        else:
            attribute = self.context['attribute']
            if Attribute.objects.filter(name__iexact=value).exclude(name=attribute.name).exists():
                error = True
        if error:
            raise serializers.ValidationError("attribute with this name already exists.")
        return value
        

class AttributeValueSerializer(serializers.ModelSerializer, TimestampMixin):
    """Attribute value model serializer."""
    attribute_id = serializers.IntegerField(min_value=1, write_only=True)
    # attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model  = AttributeValue
        fields = ["id", "name", "attribute_id"]

    def validate(self, data):
        """Validate that attribute can't have the same value twice."""
        is_create = self.context['is_create']
        name = data.get('name')
        attribute_id = data.get('attribute_id')
        error = False
        if is_create:
            if AttributeValue.objects.filter(attribute_id=attribute_id, name__iexact=name).exists():
                error = True
        else:
            attribute_value = self.context['attribute_value']
            if AttributeValue.objects.filter(attribute_id=attribute_id, name__iexact=name).exclude(
                                        attribute=attribute_value.attribute, name=attribute_value.name).exists():
                error = True
        if error:
            raise serializers.ValidationError("This attribute already has this value.")
        return data

    def create(self, validated_data):
        """Create and return a new attribute value."""
        attribute_id = validated_data.get('attribute_id')
        attribute_instance = get_object_or_404(Attribute, id=attribute_id)
        return AttributeValue.objects.create(attribute=attribute_instance, **validated_data)    

    def update(self, instance, validated_data):
        """Update attribute value."""
        attribute_id = validated_data.get('attribute_id')
        if attribute_id:
            instance.attribute = get_object_or_404(Attribute, id=attribute_id)
        instance.save()
        return super().update(instance, validated_data)


###
# Product Variant
###
class VariantAttributeValueSerializer(serializers.ModelSerializer):
    """Attribute value model serializer."""
    attribute_id = serializers.CharField(source='attribute.id', read_only=True)
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model  = AttributeValue
        fields = ["id", "name", "attribute_id", "attribute_name"]


class ProductVariantImageSerializer(serializers.ModelSerializer, TimestampMixin):
    """Product variant image model serializer."""
    image_id = serializers.IntegerField(min_value=1, write_only=True, required=False)

    class Meta:
        model  = ProductVariantImage
        fields = ["id", "image_id", "image", "is_thumbnail", "is_active", "updated_at", "created_at"]


class ProductVariantSerializer(serializers.ModelSerializer):
    """Product variant model serializer."""
    variant_id = serializers.IntegerField(min_value=1, write_only=True, required=False)
    variants = serializers.SerializerMethodField()
    images = ProductVariantImageSerializer(required=False, many=True)

    class Meta:
        model  = ProductVariant
        fields = ["id", "variant_id", "variant", "variants",  "images", "max_price", "discount_price", 
                "total_in_stock", "is_in_stock", "is_active"]
        extra_kwargs = {'variant': {'write_only': True}}

    def get_variants(self, obj):
        """Return all attribute variants for this product variant."""
        variants = AttributeValue.objects.filter(id__in=obj.variant.all())
        if variants:
            return VariantAttributeValueSerializer(variants, many=True).data
        else:
            return None 

    def validate(self, data):
        """
        Validate that existing variant obj has id & the product has this variant id, and has new variant to create new one.
        Validate that existing image obj has id & the product has this image id, and has new image to create new one.
        """
        is_update = self.context['is_update']
        variant_obj = None
        is_variant_update = False
        if is_update:
            product_obj = self.context['product_obj']
            # variant
            if 'variant_id' not in data.keys() and 'variant' not in data.keys():
                raise serializers.ValidationError({"variants": {"variant": "This list may not be empty."}})
            # variant id
            if 'variant_id' in data.keys() and data['variant_id'] not in product_obj.variants.values_list('id', flat=True):
                    raise serializers.ValidationError({"variants": {"variant_id": "This product does not have this variant id."}})
            if 'variant_id' in data.keys():
                is_variant_update = True
                variant_obj = get_object_or_404(ProductVariant, id=data.get('variant_id'))
            else:
                # required fields    
                keys_lst = ['max_price', 'total_in_stock']
                for key in keys_lst:
                    if key not in data.keys():
                        raise serializers.ValidationError({"variants": {key: "This field is required."}})
            # # total in stock
            # total_in_stock = data.get('total_in_stock')
            # product_total_in_stock = self.parent.parent.initial_data.get('total_in_stock')
            # print('total_in_stock', total_in_stock)
            # if total_in_stock:
            #     if product_total_in_stock and variant_obj:
            #         quantity_left = int(product_total_in_stock) - product_obj.variants.exclude(id=variant_obj.id).aggregate(
            #             total=Coalesce(Sum('total_in_stock'), 0))['total']
            #     elif product_total_in_stock:
            #         quantity_left = int(product_total_in_stock) - product_obj.variants.aggregate(
            #             total=Coalesce(Sum('total_in_stock'), 0))['total']
            #     elif variant_obj:  
            #         quantity_left = product_obj.total_in_stock - product_obj.variants.exclude(id=variant_obj.id).aggregate(
            #             total=Coalesce(Sum('total_in_stock'), 0))['total']
            #     else:
            #         quantity_left = product_obj.total_in_stock - product_obj.variants.aggregate(
            #             total=Coalesce(Sum('total_in_stock'), 0))['total']
            #     print('product_obj.variants.exclude(id=variant_obj.id)', product_obj.variants.aggregate(
            #             total=Coalesce(Sum('total_in_stock'), 0))['total'])
            #     # if 'variant_id' in data.keys():
            #     #     quantity_left = product_obj.total_in_stock - product_obj.variants.exclude(id=variant_obj.id).aggregate(
            #     #         total=Coalesce(Sum('total_in_stock'), 0))['total']
            #     # else:
            #     #     quantity_left = product_obj.total_in_stock - product_obj.variants.aggregate(
            #     #         total=Coalesce(Sum('total_in_stock'), 0))['total']
            #     print(product_obj.total_in_stock, quantity_left)
            #     if total_in_stock > quantity_left:
            #         raise serializers.ValidationError({"variants": {"total_in_stock": 
            #             f"Total in stock can't be greater than product total in stock value. Only {quantity_left} left"}})
            # images
            images = data.get('images')
            if images:
                for image in images:
                    file_error = False
                    if 'variant_id' not in data.keys() and 'image' not in image.keys():
                        file_error = True
                    if 'image_id' not in image.keys() and 'image' not in image.keys():
                        file_error = True
                    if file_error:
                        raise serializers.ValidationError({"images": {"image": "No file was submitted."}})
                    # image id
                    if 'image_id' in image.keys():
                        images_ids_list = []
                        for obj in product_obj.variants.all():
                            images_ids_list.extend(obj.images.values_list('id', flat=True))
                        if image['image_id'] not in images_ids_list:
                            raise serializers.ValidationError({"images": {"image_id": "This product does not have this image id."}})
        # discount price
        max_price = data.get('max_price')
        discount_price = data.get('discount_price')
        if compare_max_discount_price(max_price, discount_price, is_variant_update, instance=variant_obj):
            raise serializers.ValidationError({"variants": {"discount_price": "Discount price can't be greater than maximum price."}})
        return data

    def create(self, validated_data):
        """Create new product variant with m2m & images for variant attributes."""
        product_id = self.context['product_id']
        data = validated_data
        variant = data.pop('variant')
        images = None
        if 'images' in data:
            images = data.pop('images')
        product_variant = ProductVariant.objects.create(**data, product_id=product_id)
        product_variant.variant.set(variant)
        if images:
            for image in images:
                if 'image_id' in image.keys():
                    image_id= image.pop('image_id')
                ProductVariantImage.objects.create(**image, variant=product_variant)
        return validated_data

    def update(self, instance, validated_data):
        """Update variant & variant images of nested serializer."""
        if 'images' in validated_data:
            images = validated_data.pop('images')
            for image in images:
                # update existing images
                if 'image_id' in image.keys():
                    image_obj = get_object_or_404(ProductVariantImage, id=image['image_id'])
                    for key, value in image.items():
                        setattr(image_obj, key, value)
                    image_obj.save()    
                # create new ones
                else:
                    new_obj = ProductVariantImage.objects.create(**image, variant=instance)
        return super().update(instance, validated_data)


###
# Product
###
class ProductListSerializer(serializers.ModelSerializer):
    """Product list model serializer."""
    class Meta:
        model  = Product
        fields = ["id", "name", "slug", "description", 'max_price', 'discount_price', 'thumbnail']
        read_only_fields = ['slug']      


class ProductDetailSerializer(serializers.ModelSerializer):
    """Product detail model serializer."""
    thumbnail_url = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model  = Product
        fields = ["id", "name", "slug", "description", "details", "category", 
                'max_price', 'discount_price', 'thumbnail_url', "variants",
                "total_in_stock", "is_in_stock", "is_active", "updated_at", "created_at"]
        read_only_fields = ['slug']

    def get_thumbnail_url(self, car):
        request = self.context.get('request')
        thumbnail_url = car.thumbnail.url
        return request.build_absolute_uri(thumbnail_url)

    # def validate_discount_price(self, value):
    #     """Validate that discount price is not greater than max price."""
    #     is_update = self.context['is_update']
    #     max_price = self.get_initial().get('max_price')
    #     discount_price = value
    #     product_obj = self.context.get('product_obj')
    #     if compare_max_discount_price(max_price, discount_price, is_update, instance=product_obj):
    #         raise serializers.ValidationError("Discount price can't be greater than maximum price.")
    #     return value

    def validate(self, data):
        """Validate than total in stock of variants are not greater than total of stock of product."""
        is_update = self.context['is_update']
        product_obj = self.context.get('product_obj')        
        product_total_in_stock = data.get('total_in_stock')
        variants = data.get('variants')
        variants_total_in_stock = 0
        if is_update:
            product_obj = self.context.get('product_obj')
            entered_variants_ids_list = []
            if not product_total_in_stock:
                product_total_in_stock = product_obj.total_in_stock
            if variants:
                for variant in variants:
                    variant_id = variant.get('variant_id')
                    if variant_id:
                        entered_variants_ids_list.append(variant_id)
                    variant_total_in_stock = variant.get('total_in_stock')
                    if variant_total_in_stock:
                        variants_total_in_stock += variant_total_in_stock
            # get all variant's total in stock excluding the entered ones            
            variants_total_in_stock += product_obj.variants.exclude(id__in=entered_variants_ids_list).aggregate(
                    total=Coalesce(Sum('total_in_stock'), 0))['total']
        else:
            if variants:
                for variant in variants:
                    variants_total_in_stock += variant.get('total_in_stock')
        # validate total in stock
        if variants_total_in_stock > product_total_in_stock:
            raise serializers.ValidationError({"variants": 
                {"total_in_stock": "total in stock of variants can't be greater than total of stock of product."}})
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Create new product with variants & images for variant attributes."""
        if 'variants' in validated_data.keys():  
            variants_data = validated_data.pop('variants')
            product_obj = Product.objects.create(**validated_data)
            for variant in variants_data:
                ProductVariantSerializer.create(ProductVariantSerializer(context={"product_id": product_obj.id}), 
                                    validated_data=variant)
        else:
            product_obj = Product.objects.create(**validated_data)                            
        return product_obj

    @transaction.atomic
    def update(self, instance, validated_data):
        """Update product & variants of nested serializer."""
        if 'variants' in validated_data.keys():
            variants_data = validated_data.pop('variants')
            for data in variants_data:
                # update existing variants
                if 'variant_id' in data.keys():
                    variant_obj = get_object_or_404(ProductVariant, id=data['variant_id'])
                    ProductVariantSerializer.update(ProductVariantSerializer(), instance=variant_obj, validated_data=data)
                # create new ones
                else:
                    new_variant_obj = ProductVariantSerializer.create(ProductVariantSerializer(context={"product_id": instance.id}), 
                                    validated_data=data)
        return super().update(instance, validated_data)


###
# Question
###
class AnswerSerializer(serializers.ModelSerializer, TimestampMixin):
    """Answer model serializer."""
    user = UserSerializer(read_only=True)

    class Meta:
        model  = Answer
        fields = ["id", "user", "content", "is_active", "updated_at", "created_at"] 


class QuestionSerializer(serializers.ModelSerializer, TimestampMixin):
    """Question model serializer."""
    user = UserSerializer(read_only=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model  = Question
        fields = ["id", "user", "content", "answers", "is_active", "updated_at", "created_at"]

    def get_answers(self, obj):
        if obj.answers.exists():
            return AnswerSerializer(obj.answers.all(), many=True, context=self.context).data
        else:
            return None


###
# Review
###
class ReviewSerializer(serializers.ModelSerializer, TimestampMixin):
    """Review model serializer."""
    customer = CustomerDetailSerializer(read_only=True)

    class Meta:
        model  = Review
        fields = ["id", "customer", "title", "content", "rate", "is_active", "updated_at", "created_at"]

    def validate(self, data):
        """Validate that customer can only have one review for a product."""
        is_create = self.context['is_create']
        if is_create:
            request = self.context['request']
            product = self.context['product']
            if Review.objects.filter(customer=request.user.customer, product=product).exists():
                raise serializers.ValidationError('You can only have one review for a product')
        return data


###
# Wishlist
###
class WishlistProductListSerializer(serializers.ModelSerializer, TimestampMixin):
    """Wishlist Product List model serializer."""
    id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    slug = serializers.SlugField(source='product.slug')
    description = serializers.CharField(source='product.description')
    max_price = serializers.DecimalField(source='product.max_price', max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(source='product.discount_price', max_digits=10, decimal_places=2)

    class Meta:
        model  = Wishlist
        fields = ["id", "name", "slug", "description", "max_price", "discount_price"]