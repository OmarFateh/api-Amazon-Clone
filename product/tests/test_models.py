import pytest

from product.models import Product, Question, Answer, Review


class TestProductModel:
    
    def test_product_str(self, new_product):
        """Test product obj str method."""
        assert new_product.__str__() == 'test title'

    def test_actual_price(self, new_product):
        """Test actual price method."""
        assert new_product.actual_price == 500
        new_product.discount_price = None
        assert new_product.actual_price == 700  
    
    def test_price_discount_difference(self, new_product):
        """Test price discount difference method."""
        assert new_product.get_price_discount_difference == 200

    def test_price_discount_difference_percentage(self, new_product):
        """Test price discount difference percentage method."""
        assert new_product.get_price_discount_difference_percentage == 28


class TestQuestionModel:

    def test_question_str(self, new_question):
        """Test question obj str method."""
        assert new_question.__str__() == 'test title | testemail1@gmail.com'


class TestAnswerModel:
    
    def test_answer_str(self, new_answer):
        """Test answer obj str method."""
        assert new_answer.__str__() == 'test title | testemail1@gmail.com'


class TestReviewModel:
    
    def test_review_str(self, new_review):
        """Test review obj str method."""
        assert new_review.__str__() == 'test title | testemail@gmail.com | 5 stars'

    def test_rate_percentage(self, new_review):
        """Test rate percentage method."""
        assert new_review.get_rate_percentage == 100


class TestWishlistModel:
    
    def test_wishlist_str(self, new_wishlist):
        """Test wishlist obj str method."""
        assert new_wishlist.__str__() == 'testemail@gmail.com | test title'