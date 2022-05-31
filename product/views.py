from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from category.permissions import IsAdmin
from customer.permissions import IsCustomer, IsCustomerOwner
from merchant.permissions import IsMerchant, IsMerchantOwner, IsMerchantOwnerOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .models import Product, Attribute, AttributeValue, ProductVariant, ProductVariantImage, Question, Answer, Review, Wishlist
from .serializers import (ProductListSerializer, ProductDetailSerializer, AttributeSerializer,
                        AttributeValueSerializer, ProductVariantSerializer, ProductVariantImageSerializer,
                        QuestionSerializer, AnswerSerializer, ReviewSerializer, )


###
# Product
###
class ProductListAPIView(generics.ListAPIView):
    """Product list API view."""
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}


class ProductCreateAPIView(generics.CreateAPIView):
    """
    Merchant Product create API view.
    Only a merchant can create it.
    """
    permission_classes = [IsMerchant]
    serializer_class = ProductDetailSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Return a list of all the products
        for the currently authenticated merchant.
        """
        return Product.objects.filter(merchant=self.request.user.merchant)    

    def perform_create(self, serializer):
        """Set authenticated merchant to be the product's merchant automatically."""
        serializer.save(merchant=self.request.user.merchant)

    def get_serializer_context(self, *args, **kwargs):
        return {"is_update":False, "request":self.request}


class ProductUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Merchant Product update delete API view.
    Only the authenticated merchant owner can update or delete it.
    """
    permission_classes = [IsMerchantOwnerOrReadOnly]
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.select_related('category', 'merchant')

    def get_object(self, *args, **kwargs):
        # get product slug from the requested url.
        product_slug = self.kwargs.get("product_slug", None)
        obj = get_object_or_404(Product, slug=product_slug)
        if self.request.user.is_authenticated:   
            self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self, *args, **kwargs):
        return {"is_update":True, 'product_obj': self.get_object(), "request":self.request}


###
# Variant Attribute
### 
class AttributeListCreateAPIView(generics.ListCreateAPIView):
    """Attribute list create API view."""
    permission_classes = [IsAdmin]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"is_create":True}


class AttributeUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Attribute detail update delete API view. 
    Only the admin can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [IsAdmin]
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get_object(self, *args, **kwargs):
        # get attribute id from the requested url.
        attribute_id = self.kwargs.get("attribute_id", None)
        obj = get_object_or_404(Attribute, id=attribute_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self, *args, **kwargs):
        return {"attribute":self.get_object(), "is_create":False}


class AttributeValueListCreateAPIView(generics.ListCreateAPIView):
    """Attribute value list create API view."""
    permission_classes = [IsAdmin]
    queryset = AttributeValue.objects.select_related('attribute')
    serializer_class = AttributeValueSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"is_create":True}


class AttributeValueUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Attribute value detail update delete API view. 
    Only the admin can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [IsAdmin]
    queryset = AttributeValue.objects.select_related('attribute')
    serializer_class = AttributeValueSerializer

    def get_object(self, *args, **kwargs):
        # get attribute value id from the requested url.
        attribute_value_id = self.kwargs.get("attribute_value_id", None)
        obj = get_object_or_404(AttributeValue, id=attribute_value_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self, *args, **kwargs):
        return {"attribute_value":self.get_object(), "is_create":False}


###
# Product Variant
###
# class ProductVariantListCreateAPIView(generics.ListCreateAPIView):
#     """Product variant list create API view."""
#     permission_classes = [IsMerchant]
#     queryset = ProductVariant.objects.select_related('product')
#     serializer_class = ProductVariantSerializer

#     def get_serializer_context(self, *args, **kwargs):
#         return {"is_update":False}


# class ProductVariantUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    # """
    # Product variant detail update delete API view.
    # Only the authenticated merchant owner can update or delete it.
    # """
    # permission_classes = [IsMerchantOwner]
    # queryset = ProductVariant.objects.select_related('product')
    # serializer_class = ProductVariantSerializer

    # def get_object(self, *args, **kwargs):
    #     # get product variant id from the requested url.
    #     variant_id = self.kwargs.get("variant_id", None)
    #     obj = get_object_or_404(ProductVariant, id=variant_id)
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"is_update":True}


###
# Product Variant Image
###
# class ProductVariantListCreateAPIView(generics.ListCreateAPIView):
#     """Product variant image list create API view."""
#     permission_classes = [IsMerchant]
#     queryset = ProductVariantImage.objects.select_related('variant', 'variant__product')
#     serializer_class = ProductVariantImageSerializer


###
# Question
###
class ProductQuestionListAPIView(generics.ListAPIView):
    """Product Question list with answers API view."""
    serializer_class = QuestionSerializer
    
    def get_object(self, *args, **kwargs):
        # get product slug from the requested url.
        product_slug = self.kwargs.get("product_slug", None)
        obj = get_object_or_404(Product, slug=product_slug)
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        """Return a list of all the questions for this product."""
        return self.get_object().questions.all()


class QuestionCreateAPIView(generics.CreateAPIView):
    """
    Product Question create API view.
    Only an authenticated user can create it.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.select_related('product', 'user')

    def get_object(self, *args, **kwargs):
        # get product slug from the requested url.
        product_slug = self.kwargs.get("product_slug", None)
        obj = get_object_or_404(Product, slug=product_slug)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        """Set authenticated user to be the question's user automatically."""
        serializer.save(user=self.request.user, product=self.get_object())


class QuestionUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Product Question update delete API view.
    Only the authenticated owner can update or delete it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = QuestionSerializer
    queryset = Question.objects.select_related('product', 'user')

    def get_object(self, *args, **kwargs):
        # get question id from the requested url.
        question_id = self.kwargs.get("question_id", None)
        obj = get_object_or_404(Question, id=question_id)
        self.check_object_permissions(self.request, obj)
        return obj


class AnswerCreateAPIView(generics.CreateAPIView):
    """
    Product Question Answer create API view.
    Only an authenticated user can create it.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.select_related('question', 'user')

    def get_object(self, *args, **kwargs):
        # get question id from the requested url.
        question_id = self.kwargs.get("question_id", None)
        obj = get_object_or_404(Question, id=question_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        """Set authenticated user to be the answer's user automatically."""
        serializer.save(user=self.request.user, question=self.get_object())


class AnswerUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Product Question Answer update delete API view.
    Only the authenticated owner can update or delete it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AnswerSerializer
    queryset = Answer.objects.select_related('question', 'user')

    def get_object(self, *args, **kwargs):
        # get answer id from the requested url.
        answer_id = self.kwargs.get("answer_id", None)
        obj = get_object_or_404(Answer, id=answer_id)
        self.check_object_permissions(self.request, obj)
        return obj


###
# Review
###
class ProductReviewListAPIView(generics.ListAPIView):
    """Product Review list API view."""
    serializer_class = ReviewSerializer
    
    def get_object(self, *args, **kwargs):
        # get product slug from the requested url.
        product_slug = self.kwargs.get("product_slug", None)
        obj = get_object_or_404(Product, slug=product_slug)
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        """Return a list of all the reviews for this product."""
        return self.get_object().reviews.all()


class ReviewCreateAPIView(generics.CreateAPIView):
    """
    Product Review create API view.
    Only an authenticated user can create it.
    """
    permission_classes = [IsCustomer]
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('product', 'customer')

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request, "product":self.get_object(), "is_create":True}

    def get_object(self, *args, **kwargs):
        # get product slug from the requested url.
        product_slug = self.kwargs.get("product_slug", None)
        obj = get_object_or_404(Product, slug=product_slug)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        """Set authenticated user to be the review's user automatically."""
        serializer.save(customer=self.request.user.customer, product=self.get_object())


class ReviewUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Product Review update delete API view.
    Only the authenticated customer owner can update or delete it.
    """
    permission_classes = [IsCustomerOwner]
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('product', 'customer')

    def get_serializer_context(self, *args, **kwargs):
        return {"is_create":False}

    def get_object(self, *args, **kwargs):
        # get review id from the requested url.
        review_id = self.kwargs.get("review_id", None)
        obj = get_object_or_404(Review, id=review_id)
        self.check_object_permissions(self.request, obj)
        return obj


###
# Wishlist
###
class WishlistProductAddDeleteAPIView(APIView):
    """
    Customer Wishlist Product add delete API view.
    Only an authenticated user can add/delete it.
    """
    permission_classes = [IsCustomer]
    
    def get_object(self, *args, **kwargs):
        # get product slug from the requested url.
        product_slug = self.kwargs.get("product_slug", None)
        obj = get_object_or_404(Product, slug=product_slug)
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        """Add or delete product to or from the user's wishlist."""
        wishlist_qs = Wishlist.objects.filter(customer=request.user.customer, product=self.get_object())
        if wishlist_qs.exists():
            wishlist_obj = wishlist_qs.first()
            if wishlist_obj.is_active:
                wishlist_obj.is_active = False
                wishlist_obj.save()
                return Response({'success':'this product was deleted successfully from your wishlist.'}, 
                                status=status.HTTP_200_OK)
            else:
                wishlist_obj.is_active = True
                wishlist_obj.save()
                return Response({'success':'this product was added successfully to your wishlist.'}, 
                                status=status.HTTP_200_OK)
        else:    
            Wishlist.objects.create(customer=request.user.customer, product=self.get_object())
            return Response({'success':'this product was added successfully to your wishlist.'}, 
                            status=status.HTTP_200_OK)