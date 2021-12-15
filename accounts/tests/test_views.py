from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from customer.models import Customer
from merchant.models import Merchant
from useradmin.models import UserAdmin


class TestRegisterUSer:

    data = {"user": {'first_name': 'test', 'last_name': 'name', 'email': 'testemail@gmail.com', 
                'email2': 'testemail@gmail.com', 'password': 'admin1600', 
                'password2': 'admin1600'}}
    merchant_url = reverse('users-api:register-merchant')
    customer_url = reverse('users-api:register-customer')

    def test_register_customer_user(self, db, api_client):
        """Test register customer user response status."""
        response = api_client.post(self.customer_url, data=self.data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(user_type='C').count() == 1
        assert Customer.objects.count() == 1
        assert Customer.objects.first().user.email == self.data['user']['email']

    def test_register_merchant_user(self, db, api_client):
        """Test register merchant user response status."""
        self.data['company_name'] = 'amazon'
        self.data['gst_detail'] = 'gst detail'
        response = api_client.post(self.merchant_url, data=self.data, format='json')
        assert response.status_code == 201
        assert User.objects.filter(user_type='M').count() == 1
        assert Merchant.objects.count() == 1
        assert Merchant.objects.first().user.email == self.data['user']['email']

  
@pytest.mark.parametrize(
    "email, password, status_code", 
    [
        ('testemail@gmail.com', 'admin1600', 200),
        ('user@example.com', 'invalid_pass', 401),
    ]
)
def test_login(email, password, status_code, api_client, db):
    """Test login user response status."""
    User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
    url = reverse('users-api:login')
    data = {'email': email, 'password': password}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, is_verified, status_code", 
    [
        ('testemail@gmail.com', False, 200),
        ('testemail@gmail.com', True, 400),
        ('user@example.com', True, 400),
    ]
)
def test_request_email_verification(email, is_verified, status_code, api_client, db):
    """Test request email verification response status."""
    User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=is_verified)
    url = reverse('users-api:verfiy-email')
    data = {'email': email}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


def test_verify_email(api_client, db):
    """Test email verification response status."""
    user = User.objects.create_user(email='testemail@gmail.com', password='admin1600')
    token = str(RefreshToken.for_user(user).access_token)
    url = reverse('users-api:verfiy-email-confirm', kwargs={"token": token})
    assert user.is_verified == False
    response = api_client.get(url)
    user.refresh_from_db()
    assert response.status_code == 200
    assert user.is_verified == True


@pytest.mark.parametrize(
    "old_password, new_password1, new_password2, status_code", 
    [
        ('admin1600', 'admin160', 'admin160', 200),
        ('admin1600', 'admin160', 'admin1600', 400),
        ('admin160', 'admin16', 'admin16', 400),
    ]
)
def test_change_password(old_password, new_password1, new_password2, status_code, api_client, db):
    """Test password change response status."""
    user = User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
    api_client.force_authenticate(user)
    url = reverse('users-api:password-change')
    data = {'old_password': old_password, 'new_password1':new_password1, 'new_password2': new_password2}
    response = api_client.put(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, is_verified, status_code", 
    [
        ('testemail@gmail.com', True, 200),
        ('testemail@gmail.com', False, 400),
        ('user@example.com', True, 400),
    ]
)
def test_request_password_reset(email, is_verified, status_code, api_client, db):
    """Test request password reset response status."""
    User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=is_verified)
    url = reverse('users-api:password-reset')
    data = {'email': email}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "new_password1, new_password2, status_code", 
    [
        ('admin160', 'admin160', 200),
        ('admin160', 'admin1600', 400),
    ]
)
def test_reset_password(new_password1, new_password2, status_code, api_client, db, new_user):
    """Test password reset response status."""
    uidb64 = urlsafe_base64_encode(smart_bytes(new_user.id))
    token = str(PasswordResetTokenGenerator().make_token(new_user))
    url = reverse('users-api:password-reset-complete')
    data = {'new_password1': new_password1, 'new_password2': new_password2, 'uidb64': uidb64, 'token': token}
    response = api_client.patch(url, data=data)
    assert response.status_code == status_code