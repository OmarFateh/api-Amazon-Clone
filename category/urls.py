from django.urls import path

from .views import CategoryListAPIView, CategoryDetailAPIView, CategroyCreateAPIView, CategroyUpdateDeleteAPIView


"""
CLIENT
BASE ENDPOINT /api/categories/
"""

urlpatterns = [
    path('list/', CategoryListAPIView.as_view(), name='list'),
    path('create/', CategroyCreateAPIView.as_view(), name='create'),
    path('<path:category_slug>/update/delete/', CategroyUpdateDeleteAPIView.as_view(), name='update-delete'),
    path('<path:category_slug>/', CategoryDetailAPIView.as_view(), name='detail'), 
        
]