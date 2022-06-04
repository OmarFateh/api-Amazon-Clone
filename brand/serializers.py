from django.shortcuts import get_object_or_404

from rest_framework import serializers

from product.mixins import TimestampMixin
from product.models import Product
from product.serializers import ProductListSerializer
from .models import Brand


class BrandSerializer(serializers.ModelSerializer, TimestampMixin):
    """Brand model serializer."""
    thumbnail_url = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model  = Brand
        fields = ["id", "name", "slug", "thumbnail", "thumbnail_url", "products", "updated_at", "created_at"]
        read_only_fields = ['slug', 'thumbnail_url']
        extra_kwargs = {"thumbnail": {'write_only': True}}

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        thumbnail_url = obj.thumbnail.url
        return request.build_absolute_uri(thumbnail_url)

    def get_products(self, obj):
        # get all products of this brand
        products = Product.objects.get_brand_products(obj)
        if products:
            return ProductListSerializer(products, many=True, context=self.context).data
        else:
            return None    


    # def validate(self, data):
    #     """Validate that a parent category can't have the same child category twice."""
    #     is_create = self.context['is_create']
    #     name = data.get('name')
    #     parent_id = data.get('parent_id')
    #     if is_create:
    #         if Category.objects.filter(parent_id=parent_id, name__iexact=name).exists():
    #             raise serializers.ValidationError("This category already exists with this parent category")
    #     else:
    #         category = self.context['category']
    #         if Category.objects.filter(parent_id=parent_id, name=name).exclude(
    #                                     parent=category.parent, name=category.name).exists():
    #             raise serializers.ValidationError("This category already exists with this parent category")
    #     return data

    # def create(self, validated_data):
    #     parent_id = validated_data.get('parent_id')
    #     if parent_id:
    #         category_instance = get_object_or_404(Category, id=parent_id)
    #         return Category.objects.create(parent=category_instance, **validated_data)
    #     else:
    #         return Category.objects.create(**validated_data)   

    # def update(self, instance, validated_data):
    #     parent_id = validated_data.get('parent_id')
    #     if parent_id:
    #         category_instance = get_object_or_404(Category, id=parent_id)
    #         instance.category = category_instance
    #         instance.save()
    #     return super().update(instance, validated_data)


class BrandListSerializer(serializers.ModelSerializer):
    """Brand list model serializer."""
    class Meta:
        model  = Brand
        fields = ["id", "name", "slug", "thumbnail"]