from django.urls import path

from .views import CategoryListAPIView, CategoryCreateAPIView, CategoryUpdateDeleteAPIView


"""
CLIENT
BASE ENDPOINT /api/categories/
"""

urlpatterns = [
    path('list/', CategoryListAPIView.as_view(), name='list'),
    path('create/', CategoryCreateAPIView.as_view(), name='create'),
    path('<path:category_slug>/', CategoryUpdateDeleteAPIView.as_view(), name='detail-update-delete'),        
]