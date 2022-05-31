from django.shortcuts import get_object_or_404

from rest_framework import serializers

from product.mixins import TimestampMixin
from product.models import Product
from product.serializers import ProductListSerializer
from .mixins import ChildrenCategoriesMixin
from .base_serializers import ChildrenCategorySerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer, ChildrenCategoriesMixin, TimestampMixin):
    """Category model serializer."""
    thumbnail_url = serializers.SerializerMethodField()
    root_category = serializers.SerializerMethodField()
    parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "thumbnail_url", "description", 'parent_id', "root_category", 
                "children_categories", "products", "updated_at", "created_at"]
        read_only_fields = ['slug']
        extra_kwargs = {"parent_id": {'write_only': True}}

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        thumbnail_url = obj.thumbnail.url
        return request.build_absolute_uri(thumbnail_url)

    def get_root_category(self, obj):
        if not obj.is_root_node():
            return ChildrenCategorySerializer(obj.get_root(), context=self.context).data
        else:
            return None

    def get_products(self, obj):
        # get all products of descendants categories of this category
        products = Product.objects.get_descendants_products(obj)
        if products:
            return ProductListSerializer(products, many=True, context=self.context).data
        else:
            return None    

    def validate_parent_id(self, value):
        """Validate parent category."""
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

    def validate(self, data):
        """Validate that a parent category can't have the same child category twice."""
        is_create = self.context['is_create']
        name = data.get('name')
        parent_id = data.get('parent_id')
        if is_create:
            if Category.objects.filter(parent_id=parent_id, name__iexact=name).exists():
                raise serializers.ValidationError("This category already exists with this parent category")
        else:
            category = self.context['category']
            if Category.objects.filter(parent_id=parent_id, name=name).exclude(
                                        parent=category.parent, name=category.name).exists():
                raise serializers.ValidationError("This category already exists with this parent category")
        return data

    def create(self, validated_data):
        parent_id = validated_data.get('parent_id')
        if parent_id:
            category_instance = get_object_or_404(Category, id=parent_id)
            return Category.objects.create(parent=category_instance, **validated_data)
        else:
            return Category.objects.create(**validated_data)   

    def update(self, instance, validated_data):
        parent_id = validated_data.get('parent_id')
        if parent_id:
            category_instance = get_object_or_404(Category, id=parent_id)
            instance.category = category_instance
            instance.save()
        return super().update(instance, validated_data)


class CategoryListSerializer(serializers.ModelSerializer, ChildrenCategoriesMixin):
    """Category list model serializer."""
    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "thumbnail", "children_categories"]