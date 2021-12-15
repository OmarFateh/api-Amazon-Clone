import json
import os

from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from product.models import Attribute, AttributeValue, Product, Question, Answer, Review, Wishlist


class TestVariantAttribute:

    list_create_endpoint = reverse('product-api:attribute-list-create')
    update_delete_endpoint = reverse('product-api:attribute-update-delete',
                                        kwargs={"attribute_id": 1})
    data = {'name': 'test attribute'}

    def test_attribute_list(self, db, new_admin_user, new_attribute, api_client):
        """Test attribute retrieve list response status."""
        api_client.force_authenticate(new_admin_user)
        response = api_client.get(self.list_create_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_attribute_create(self, db, new_admin_user, api_client):
        """Test attribute create response status."""
        api_client.force_authenticate(new_admin_user)
        assert Attribute.objects.count() == 0
        response = api_client.post(self.list_create_endpoint, self.data)
        assert response.status_code == 201
        assert Attribute.objects.count() == 1

    def test_attribute_detail(self, db, new_admin_user, new_attribute, api_client):
        """Test attribute detail response status."""
        api_client.force_authenticate(new_admin_user)
        response = api_client.get(self.update_delete_endpoint, format='json')
        assert response.status_code == 200

    def test_attribute_update(self, db, new_admin_user, new_attribute, api_client):
        """Test attribute update response status."""
        api_client.force_authenticate(new_admin_user)
        assert new_attribute.name == 'test attribute'
        data = {'name': 'test attribute 2'}
        response = api_client.patch(self.update_delete_endpoint, data)
        new_attribute.refresh_from_db()
        assert response.status_code == 200
        assert new_attribute.name == 'test attribute 2'.title()

    def test_attribute_delete(self, db, new_admin_user, new_attribute, api_client):
        """Test attribute delete response status."""
        api_client.force_authenticate(new_admin_user)
        assert Attribute.objects.count() == 1
        response = api_client.delete(self.update_delete_endpoint)
        assert response.status_code == 204
        assert Attribute.objects.count() == 0


class TestVariantAttributeValue:
    
    list_create_endpoint = reverse('product-api:attribute-value-list-create')
    update_delete_endpoint = reverse('product-api:attribute-value-update-delete',
                                        kwargs={"attribute_value_id": 1})
    data = {'name': 'test attribute', 'attribute_id': 1}

    def test_attribute_value_list(self, db, new_admin_user, new_attribute_value, api_client):
        """Test attribute value retrieve list response status."""
        api_client.force_authenticate(new_admin_user)
        response = api_client.get(self.list_create_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_attribute_value_create(self, db, new_admin_user, new_attribute,  api_client):
        """Test attribute value create response status."""
        api_client.force_authenticate(new_admin_user)
        assert AttributeValue.objects.count() == 0
        response = api_client.post(self.list_create_endpoint, self.data)
        assert response.status_code == 201
        assert AttributeValue.objects.count() == 1

    def test_attribute_value_detail(self, db, new_admin_user, new_attribute_value, api_client):
        """Test attribute value detail response status."""
        api_client.force_authenticate(new_admin_user)
        response = api_client.get(self.update_delete_endpoint, format='json')
        assert response.status_code == 200

    def test_attribute_value_update(self, db, new_admin_user, new_attribute_value, api_client):
        """Test attribute update response status."""
        api_client.force_authenticate(new_admin_user)
        assert new_attribute_value.name == 'test attribute value'
        data = {'name': 'test attribute value 2'}
        response = api_client.patch(self.update_delete_endpoint, data)
        new_attribute_value.refresh_from_db()
        assert response.status_code == 200
        assert new_attribute_value.name == 'test attribute value 2'.title()

    def test_attribute_value_delete(self, db, new_admin_user, new_attribute_value, api_client):
        """Test attribute delete response status."""
        api_client.force_authenticate(new_admin_user)
        assert AttributeValue.objects.count() == 1
        response = api_client.delete(self.update_delete_endpoint)
        assert response.status_code == 204
        assert AttributeValue.objects.count() == 0


class TestProduct:

    product_list_endpoint = reverse('product-api:product-list')
    # merchant_product_list_endpoint = reverse('product-api:my-product-list')
    product_create_endpoint = reverse('product-api:product-create')
    product_detail_endpoint = reverse(
        'product-api:product-detail', kwargs={"product_slug": 'test-title'})
    product_update_delete_endpoint = reverse(
        'product-api:product-update-delete', kwargs={"product_slug": 'test-title'})
    upload_file = open(os.path.join(settings.BASE_DIR,
                                    'static/img/no_avatar.jpg'), "rb")
    image = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    data = {'merchant': 1, 'category': 1, 'name': 'title', 'description': 'description', 'details': 'details',
        'max_price': 700, 'discount_price': 500, 'total_in_stock': 50, 
        'is_in_stock': True, 'is_active': True, 'variants':[{'variant': [1], 
            "max_price": 60, "discount_price": 50, "total_in_stock": 20, 
            "is_in_stock": True, "is_active": True, 'images':[{'image': image}]}]}
    
    def test_product_list(self, db, new_product, api_client):
        """Test product retrieve list response status."""
        response = api_client.get(self.product_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    # def test_merchant_product_list(self, db, new_merchant_user, new_product, api_client):
    #     """Test merchant product retrieve list response status."""
    #     api_client.force_authenticate(new_merchant_user)
    #     response = api_client.get(self.merchant_product_list_endpoint, format='json')
    #     assert response.status_code == 200
    #     assert len(json.loads(response.content)) == 1

    def test_product_create(self, db, new_merchant_user, new_parent_category, api_client):
        """Test product create response status."""
        api_client.force_authenticate(new_merchant_user)
        assert Product.objects.count() == 0
        response = api_client.post(self.product_create_endpoint, self.data)
        assert response.status_code == 201
        assert Product.objects.count() == 1

    def test_product_detail(self, db, new_product, api_client):
        """Test product detail response status."""
        response = api_client.get(self.product_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_product_update(self, db, new_merchant_user, new_product, api_client):
        """Test product update response status."""
        api_client.force_authenticate(new_merchant_user)
        assert new_product.name == 'test title'
        data = {'name': 'test title 2'}
        response = api_client.patch(self.product_update_delete_endpoint, data)
        new_product.refresh_from_db()
        assert response.status_code == 200
        assert new_product.name == 'test title 2'

    def test_product_delete(self, db, new_merchant_user, new_product, api_client):
        """Test product delete response status."""
        api_client.force_authenticate(new_merchant_user)
        assert Product.objects.count() == 1
        response = api_client.delete(self.product_update_delete_endpoint)
        assert response.status_code == 204
        assert Product.objects.count() == 0 


class TestQuestion:
    
    question_list_endpoint = reverse('product-api:product-question-list', kwargs={"product_slug": 'test-title'})
    question_create_endpoint = reverse('product-api:product-question-create', kwargs={"product_slug": 'test-title'})
    question_detail_endpoint = reverse('product-api:question-update-delete', kwargs={"question_id": 1})
    data = {'product': 1, 'user': 1, 'content': 'content', 'is_active': True}
    
    def test_question_list(self, db, new_question, api_client):
        """Test question retrieve list response status."""
        response = api_client.get(self.question_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_question_create(self, db, new_merchant_user, new_product, api_client):
        """Test question create response status."""
        api_client.force_authenticate(new_merchant_user)
        assert Question.objects.count() == 0
        response = api_client.post(self.question_create_endpoint, self.data)
        assert response.status_code == 201
        assert Question.objects.count() == 1

    def test_question_detail(self, db, new_question, api_client):
        """Test question detail response status."""
        response = api_client.get(self.question_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_question_update(self, db, new_merchant_user, new_question, api_client):
        """Test question update response status."""
        api_client.force_authenticate(new_merchant_user)
        assert new_question.content == 'question content'
        data = {'content': 'question content 2'}
        response = api_client.patch(self.question_detail_endpoint, data)
        new_question.refresh_from_db()
        assert response.status_code == 200
        assert new_question.content == 'question content 2'

    def test_question_delete(self, db, new_merchant_user, new_question, api_client):
        """Test question delete response status."""
        api_client.force_authenticate(new_merchant_user)
        assert Question.objects.count() == 1
        response = api_client.delete(self.question_detail_endpoint)
        assert response.status_code == 204
        assert Question.objects.count() == 0 


class TestAnswer:
    
    answer_create_endpoint = reverse('product-api:product-question-answer-create', kwargs={"question_id": 1})
    answer_detail_endpoint = reverse('product-api:answer-update-delete', kwargs={"answer_id": 1})
    data = {'question': 1, 'user': 1, 'content': 'content', 'is_active': True}

    def test_answer_create(self, db, new_merchant_user, new_question, api_client):
        """Test answer create response status."""
        api_client.force_authenticate(new_merchant_user)
        assert Answer.objects.count() == 0
        response = api_client.post(self.answer_create_endpoint, self.data)
        assert response.status_code == 201
        assert Answer.objects.count() == 1

    def test_answer_detail(self, db, new_answer, api_client):
        """Test answer detail response status."""
        response = api_client.get(self.answer_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_answer_update(self, db, new_merchant_user, new_answer, api_client):
        """Test answer update response status."""
        api_client.force_authenticate(new_merchant_user)
        assert new_answer.content == 'answer content'
        data = {'content': 'answer content 2'}
        response = api_client.patch(self.answer_detail_endpoint, data)
        new_answer.refresh_from_db()
        assert response.status_code == 200
        assert new_answer.content == 'answer content 2'

    def test_answer_delete(self, db, new_merchant_user, new_answer, api_client):
        """Test answer delete response status."""
        api_client.force_authenticate(new_merchant_user)
        assert Answer.objects.count() == 1
        response = api_client.delete(self.answer_detail_endpoint)
        assert response.status_code == 204
        assert Answer.objects.count() == 0


class TestReview:
    
    review_list_endpoint = reverse('product-api:product-review-list', kwargs={"product_slug": 'test-title'})
    review_create_endpoint = reverse('product-api:product-review-create', kwargs={"product_slug": 'test-title'})
    review_detail_endpoint = reverse('product-api:review-update-delete', kwargs={"review_id": 1})
    data = {'product': 1, 'customer': 1, 'title': 'title', 'content': 'content', 'is_active': True}
    
    def test_review_list(self, db, new_review, api_client):
        """Test review retrieve list response status."""
        response = api_client.get(self.review_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_review_create(self, db, new_customer_user, new_product, api_client):
        """Test review create response status."""
        api_client.force_authenticate(new_customer_user)
        assert Review.objects.count() == 0
        response = api_client.post(self.review_create_endpoint, self.data)
        assert response.status_code == 201
        assert Review.objects.count() == 1

    def test_review_detail(self, db, new_customer_user, new_review, api_client):
        """Test review detail response status."""
        api_client.force_authenticate(new_customer_user)
        response = api_client.get(self.review_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_review_update(self, db, new_customer_user, new_review, api_client):
        """Test review update response status."""
        api_client.force_authenticate(new_customer_user)
        assert new_review.content == 'review content'
        data = {'content': 'review content 2'}
        response = api_client.patch(self.review_detail_endpoint, data)
        new_review.refresh_from_db()
        assert response.status_code == 200
        assert new_review.content == 'review content 2'

    def test_review_delete(self, db, new_customer_user, new_review, api_client):
        """Test review delete response status."""
        api_client.force_authenticate(new_customer_user)
        assert Review.objects.count() == 1
        response = api_client.delete(self.review_detail_endpoint)
        assert response.status_code == 204
        assert Review.objects.count() == 0 


class TestWishlist:
    
    wishlist_add_delete_endpoint = reverse('product-api:add-delete-wishlist', kwargs={"product_slug": 'test-title'})
    data = {'product': 1, 'customer': 1, 'is_active': True}

    def test_wishlist_add_delete(self, db, new_customer_user, new_customer, new_product, api_client):
        """Test wishlist add/delete response status."""
        api_client.force_authenticate(new_customer_user)
        assert Wishlist.objects.count() == 0
        # add product to wishlist
        response = api_client.post(self.wishlist_add_delete_endpoint, self.data)
        wishlist_qs = Wishlist.objects.filter(product=new_product, customer=new_customer)
        assert response.status_code == 200
        assert Wishlist.objects.count() == 1
        assert wishlist_qs.count() == 1
        assert wishlist_qs.first().is_active == True
        # remove product from wishlist & set it to be inactive
        response = api_client.post(self.wishlist_add_delete_endpoint, self.data)
        assert response.status_code == 200
        assert wishlist_qs.first().is_active == False