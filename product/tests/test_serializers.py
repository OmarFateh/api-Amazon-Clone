import os

from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from product.serializers import (AttributeSerializer, AttributeValueSerializer, QuestionSerializer, 
                                ProductVariantSerializer, ProductDetailSerializer, 
                                AnswerSerializer, ReviewSerializer,)


class TestAttributeSerializer:

    data = {'name': 'test attribute'}

    def test_create_valid_serializer(self, db):
        """Test valid create attribute serializer data."""
        serializer = AttributeSerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == True

    def test_create_attribute_already_exists(self, db, new_attribute):
        """Test attribute already exists in create view."""
        serializer = AttributeSerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == False
        assert serializer.errors['name'][0] == 'attribute with this name already exists.'

    def test_update_attribute_already_exists(self, db, new_attribute):
        """Test attribute already exists in update view."""
        serializer = AttributeSerializer(data=self.data, instance=new_attribute,
                        context={'is_create': False, 'attribute': new_attribute})
        assert serializer.is_valid() == True


class TestAttributeValueSerializer:

    data = {'name': 'test attribute value', 'attribute_id': 1}

    def test_create_valid_serializer(self, db, new_attribute):
        """Test valid create attribute value serializer data."""
        serializer = AttributeValueSerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == True

    def test_create_attribute_value_already_exists(self, db, new_attribute, new_attribute_value):
        """Test attribute value with this attribute already exists in create view."""
        serializer = AttributeValueSerializer(data=self.data, context={'is_create': True})
        assert serializer.is_valid() == False
        assert serializer.errors['non_field_errors'][0] == 'This attribute already has this value.'

    def test_create_attribute_value_already_exists(self, db, new_attribute, new_attribute_value):
        """Test attribute value with this attribute already exists in update view."""
        serializer = AttributeValueSerializer(data=self.data, instance=new_attribute_value,
                        context={'is_create': False, 'attribute_value': new_attribute_value})
        assert serializer.is_valid() == True


class TestProductVariantSerializer:

    upload_file = open(os.path.join(settings.BASE_DIR,
                                    'static/img/no_avatar.jpg'), "rb")
    image = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    data = {'variant': [1], "max_price": 60, "discount_price": 50,
                "total_in_stock": 20, "is_in_stock": True, "is_active": True}

    def test_create_valid_serializer(self, db, new_attribute_value):
        """Test valid create product variant serializer data."""
        serializer = ProductVariantSerializer(data=self.data, context={'is_update': False})
        assert serializer.is_valid() == True

    def test_create_discount_exceeds_max_price(self, db, new_attribute_value):
        """Test discount exceeds max price in create view."""
        self.data['max_price'] = 40
        serializer = ProductVariantSerializer(data=self.data, context={'is_update': False})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['discount_price'] == "Discount price can't be greater than maximum price."
        self.data['max_price'] = 60

    def test_create_image_not_submitted(self, db):
        """test image not submitted in create view."""
        self.data["images"] = [{"is_active": True}]
        serializer = ProductVariantSerializer(data=self.data, context={'is_update': False})
        assert serializer.is_valid() == False
        assert serializer.errors['images'][0]['image'][0] == "No file was submitted."

    def test_update_empty_variant_id(self, db, new_attribute_value, new_product_variant, new_product):
        """Test variant & variant id not given in update view."""
        del self.data['variant']
        serializer = ProductVariantSerializer(data=self.data, instance=new_product_variant, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['variant'] == "This list may not be empty."
        self.data['variant'] = [1]

    def test_update_wrong_variant_id(self, db, new_attribute_value, new_product_variant, new_product):
        """Test variant id is not in product's variants in update view."""
        self.data['variant_id'] = 5
        serializer = ProductVariantSerializer(data=self.data, instance=new_product_variant, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['variant_id'] == "This product does not have this variant id."
        del self.data['variant_id']
    
    def test_update_fields_required(self, db, new_attribute_value, new_product_variant, new_product):
        """Test required fields are not given while variant id in not given in update view."""
        del self.data['max_price']
        serializer = ProductVariantSerializer(data=self.data, instance=new_product_variant, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['max_price'] == 'This field is required.'
        self.data['max_price'] = 60

    def test_update_image_not_submitted(self, db, new_attribute_value, new_product_variant, new_product):
        """test image & image id not submitted in update view."""
        self.data["images"] = [{"is_active": True}]
        serializer = ProductVariantSerializer(data=self.data, instance=new_product_variant, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['images']['image'] == "No file was submitted."

    def test_update_wrong_image_id(self, db, new_attribute_value, new_product_variant, new_product):
        """Test image id is not in product variant's images in update view."""
        self.data['variant_id'] = 1
        self.data["images"] = [{"image_id": 5, "is_active": True}]
        serializer = ProductVariantSerializer(data=self.data, instance=new_product_variant, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['images']['image_id'] == "This product does not have this image id."


class TestProductSerializer:

    upload_file = open(os.path.join(settings.BASE_DIR,
                                    'static/img/no_avatar.jpg'), "rb")
    image = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    data = {'merchant': 1, 'category': 1, 'name': 'title', 'description': 'description', 
            'details': 'details', 'total_in_stock': 50, 'is_in_stock': True, 'is_active': True, 
            'variants':[{'variant': [1], "max_price": 60, "discount_price": 50, "total_in_stock": 20, 
            "is_in_stock": True, "is_active": True, 'images':[{'image': image}]}]}

    def test_create_valid_serializer(self, db, new_parent_category, new_attribute_value, new_product_variant, new_merchant):
        """Test valid create product serializer data."""
        serializer = ProductDetailSerializer(data=self.data, context={'is_update': False})
        assert serializer.is_valid() == True

    # def test_create_discount_exceeds_max_price(self, db, new_parent_category, new_attribute_value, new_product_variant, new_merchant):
    #     """Test discount exceeds max price in create view."""
    #     self.data['max_price'] = 400
    #     serializer = ProductDetailSerializer(data=self.data, context={'is_update': False})
    #     assert serializer.is_valid() == False
    #     assert serializer.errors['discount_price'][0] == "Discount price can't be greater than maximum price."
    #     self.data['max_price'] = 700

    def test_create_bigger_total_in_stock(self, db, new_parent_category, new_attribute_value, new_product_variant, new_merchant):
        """Test variant's total in stock exceeds product's total in stock in create view."""
        self.data['total_in_stock'] = 10
        serializer = ProductDetailSerializer(data=self.data, context={'is_update': False})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['total_in_stock'] == "total in stock of variants can't be greater than total of stock of product."
        self.data['total_in_stock'] = 50

    def test_update_bigger_total_in_stock(self, db, new_parent_category, new_attribute_value, new_product_variant, new_product, new_merchant):
        """Test variant's total in stock exceeds product's total in stock in update view."""
        # update current product
        data = {'total_in_stock': 5}
        serializer = ProductDetailSerializer(data=data, instance=new_product, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['total_in_stock'] == "total in stock of variants can't be greater than total of stock of product."
        # add new variant while updating
        data = {'variants':[{"variant": [1], 'total_in_stock': 50, 'max_price': 60}]}
        serializer = ProductDetailSerializer(data=data, instance=new_product, partial=True,
                        context={'is_update': True, "product_obj": new_product})
        assert serializer.is_valid() == False
        assert serializer.errors['variants']['total_in_stock'] == "total in stock of variants can't be greater than total of stock of product."


class TestQuestionSerializer:

    data = {'content': 'test question'}

    def test_create_valid_serializer(self, db, new_customer_user, new_product):
        """Test valid create question serializer data."""
        serializer = QuestionSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestAnswerSerializer:
    
    data = {'content': 'test answer'}
    url = reverse('product-api:product-question-answer-create', kwargs={"question_id": 1})

    def test_create_valid_serializer(self, db, new_customer_user, new_question, api_factory):
        """Test valid create question serializer data."""
        request = api_factory.get(self.url)
        request.user = new_customer_user
        serializer = AnswerSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestReviewSerializer:
    
    data = {'title': 'test review', 'content': 'test review', 'rate': 2}
    url = reverse('product-api:product-review-create', kwargs={"product_slug": 'test-title'})

    def test_create_valid_serializer(self, db, new_customer_user, new_product, api_factory):
        """Test valid create review serializer data."""
        request = api_factory.get(self.url)
        request.user = new_customer_user
        serializer = ReviewSerializer(data=self.data, 
                        context={"request": request, 'product': new_product, 'is_create': True})
        assert serializer.is_valid() == True

    def test_create_user_has_already_review(self, db, new_customer_user, new_product, new_review, api_factory):
        """Test user can only add one review for a product."""
        request = api_factory.get(self.url)
        request.user = new_customer_user
        serializer = ReviewSerializer(data=self.data, 
                        context={"request": request, 'product': new_product, 'is_create': True})
        assert serializer.is_valid() == False
        assert serializer.errors['non_field_errors'][0] == 'You can only have one review for a product'

    def test_update_user_has_already_review(self, db, new_customer_user, new_product, new_review, api_factory):
        """Test user can update review for a product."""
        request = api_factory.get(self.url)
        request.user = new_customer_user
        serializer = ReviewSerializer(data=self.data, instance=new_review,
                        context={"request": request, 'product': new_product, 'is_create': False})
        assert serializer.is_valid() == True