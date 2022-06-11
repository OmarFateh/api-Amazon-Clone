from rest_framework import serializers

from .base_serializers import ChildrenCategorySerializer


class ChildrenCategoriesMixin(serializers.Serializer):
    """Children categories serializer mixin."""
    children_categories = serializers.SerializerMethodField()

    def get_children_categories(self, obj):
        if obj.get_children():
            return ChildrenCategorySerializer(obj.get_children(), many=True, context=self.context).data
        else:
            return []