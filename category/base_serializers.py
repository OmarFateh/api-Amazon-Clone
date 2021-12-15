from rest_framework import serializers

from .models import Category


class ChildrenCategorySerializer(serializers.ModelSerializer):
    """Children Category list model serializer."""
    class Meta:
        model  = Category
        fields = ["id", "name", "slug", "thumbnail"]