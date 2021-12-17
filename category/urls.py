from django.urls import path

from .views import CategoryListAPIView, CategroyCreateAPIView, CategroyUpdateDeleteAPIView


"""
CLIENT
BASE ENDPOINT /api/categories/
"""

urlpatterns = [
    path('list/', CategoryListAPIView.as_view(), name='list'),
    path('create/', CategroyCreateAPIView.as_view(), name='create'),
    path('<path:category_slug>/', CategroyUpdateDeleteAPIView.as_view(), name='detail-update-delete'),        
]