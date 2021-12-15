from django.urls import path

from .views import (AttributeListCreateAPIView, AttributeUpdateDeleteAPIView, AttributeValueListCreateAPIView, 
                    AttributeValueUpdateDeleteAPIView,# ProductVariantListCreateAPIView, ProductVariantUpdateDeleteAPIView,
                    ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView, ProductUpdateDeleteAPIView, 
                    ProductQuestionListAPIView, QuestionCreateAPIView, QuestionUpdateDeleteAPIView,
                    AnswerCreateAPIView, AnswerUpdateDeleteAPIView, ProductReviewListAPIView,
                    ReviewCreateAPIView, ReviewUpdateDeleteAPIView, WishlistProductAddDeleteAPIView)


"""
CLIENT
BASE ENDPOINT /api/products/
"""

urlpatterns = [
    # Variant Attribute
    path('attributes/', AttributeListCreateAPIView.as_view(), name='attribute-list-create'),
    path('attributes/<int:attribute_id>/', AttributeUpdateDeleteAPIView.as_view(), name='attribute-update-delete'),
    path('attributes/values/', AttributeValueListCreateAPIView.as_view(), name='attribute-value-list-create'),
    path('attributes/values/<int:attribute_value_id>/', AttributeValueUpdateDeleteAPIView.as_view(), name='attribute-value-update-delete'),
    # Product Variant
    # path('variants/', ProductVariantListCreateAPIView.as_view(), name='product-variant-list-create'),
    # path('variants/<int:variant_id>/', ProductVariantUpdateDeleteAPIView.as_view(), name='product-variant-update-delete'),
    # Product
    path('list/', ProductListAPIView.as_view(), name='product-list'),
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('<str:product_slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('<str:product_slug>/update/delete/', ProductUpdateDeleteAPIView.as_view(), name='product-update-delete'),
    # Question
    path('<str:product_slug>/questions/', ProductQuestionListAPIView.as_view(), name='product-question-list'),
    path('<str:product_slug>/questions/create/', QuestionCreateAPIView.as_view(), name='product-question-create'),
    path('questions/<int:question_id>/', QuestionUpdateDeleteAPIView.as_view(), name='question-update-delete'),
    path('questions/<int:question_id>/answers/create/', AnswerCreateAPIView.as_view(), name='product-question-answer-create'),
    path('answers/<int:answer_id>/', AnswerUpdateDeleteAPIView.as_view(), name='answer-update-delete'),
    # Review
    path('<str:product_slug>/reviews/', ProductReviewListAPIView.as_view(), name='product-review-list'),
    path('<str:product_slug>/reviews/create/', ReviewCreateAPIView.as_view(), name='product-review-create'),
    path('reviews/<int:review_id>/', ReviewUpdateDeleteAPIView.as_view(), name='review-update-delete'),
    # Wishlist
    path('<str:product_slug>/wishlist/add/delete/', WishlistProductAddDeleteAPIView.as_view(), name='add-delete-wishlist'),

]