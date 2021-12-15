from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category
from .permissions import IsAdmin
from .serializers import CategorySerializer, CategoryListSerializer


class CategoryListAPIView(generics.ListAPIView):
    """Category list API view."""
    queryset = Category.objects.root_nodes()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """Category detail API view."""
    queryset = Category.objects.select_related('parent')
    serializer_class = CategorySerializer
    
    def get_object(self, *args, **kwargs):
        # get category slug from the requested url.
        category_slug = self.kwargs.get("category_slug", None)
        obj = get_object_or_404(Category, slug=category_slug)
        self.check_object_permissions(self.request, obj)
        return obj


class CategroyCreateAPIView(generics.CreateAPIView):
    """
    Category create API view.
    Only the admin can create it.
    """
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Category.objects.select_related('parent')
    serializer_class = CategorySerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"is_create": True}


class CategroyUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Category update delete API view.
    Only the admin can update or delete it.
    """
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Category.objects.select_related('parent')
    serializer_class = CategorySerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"category": self.get_object(), "is_create":False}

    def get_object(self, *args, **kwargs):
        # get category slug from the requested url.
        category_slug = self.kwargs.get("category_slug", None)
        obj = get_object_or_404(Category, slug=category_slug)
        self.check_object_permissions(self.request, obj)
        return obj