from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions

from .models import Brand
from .serializers import BrandSerializer, BrandListSerializer
from category.permissions import IsAdmin, IsAdminOrReadOnly


class BrandListAPIView(generics.ListAPIView):
    """Brand list API view."""
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    

class BrandCreateAPIView(generics.CreateAPIView):
    """
    Brand create API view.
    Only the admin can create it.
    """
    permission_classes = [IsAdmin]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"is_create": True, "request":self.request}


class BrandUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Category update delete API view.
    Only the admin can update or delete it.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"brand": self.get_object(), "is_create":False, "request":self.request}

    def get_object(self, *args, **kwargs):
        # get brand slug from the requested url.
        brand_slug = self.kwargs.get("brand_slug", None)
        obj = get_object_or_404(Brand, slug=brand_slug)
        self.check_object_permissions(self.request, obj)
        return obj   
    