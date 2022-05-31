from django.urls import path

from .views import BrandListAPIView, BrandCreateAPIView, BrandUpdateDeleteAPIView


"""
CLIENT
BASE ENDPOINT /api/brands/
"""

urlpatterns = [
    path('list/', BrandListAPIView.as_view(), name='list'),
    path('create/', BrandCreateAPIView.as_view(), name='create'),
    path('<path:brand_slug>/', BrandUpdateDeleteAPIView.as_view(), name='detail-update-delete'),        
]