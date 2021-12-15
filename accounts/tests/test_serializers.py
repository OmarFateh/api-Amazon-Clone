from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from accounts.models import User
from accounts.serializers import (UserSerializer, RequestEmailVerificationEmailSerializer, 
                                    UserLoginSerializer, PassowordChangeSerializer,
                                    RequestPasswordResetEmailSerializer, PasswordResetSerializer)


class TestUserSerializer:
    
    data = {'first_name': 'test', 'last_name': 'name', 'email': 'testemail@gmail.com', 
            'email2': 'testemail@gmail.com', 'user_type': 'C', 'password': 'admin1600', 
            'password2': 'admin1600'}

    def test_valid_serializer(self, db):
        """Test valid user serializer data."""
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == True

    def test_emails_mismatch(self, db):
        """Test two emails don't match."""
        self.data['email2'] = 'testemail2@gmail.com'
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'The two Emails must match.'
        self.data['email2'] = 'testemail@gmail.com'

    def test_email_exists(self, db):
        """Test email already exists."""
        User.objects.create_user(email='testemail@gmail.com', password='admin1600')
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'user with this email already exists.'

    def test_passwords_mismatch(self, db):
        """Test two password don't match."""
        self.data['password2'] = 'admin160'
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['password'][0] == 'The two Passwords must match.'

    def test_password_invalid(self, db):
        """Test password is invalid."""
        self.data['password'] = 'admin'
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid() == False


class TestRequestEmailVerificationEmailSerializer:

    data = {'email': 'testemail@gmail.com'}

    def test_valid_serializer(self, db):
        """Test valid serializer data."""
        # data is valid
        User.objects.create_user(email='testemail@gmail.com', password='admin1600')
        serializer = RequestEmailVerificationEmailSerializer(data=self.data)
        assert serializer.is_valid() == True
    
    def test_email_incorrect(self, db):
        """Test invalid email value data."""
        self.data['email'] = 'testemail0@gmail.com'
        User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
        serializer = RequestEmailVerificationEmailSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'Email is incorrect.'

    def test_account_inactive(self, db):
        """Test inactive account."""
        self.data['email'] = 'testemail@gmail.com'
        User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
        serializer = RequestEmailVerificationEmailSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'Account is already activated.'    
       

class TestLoginSerializer:
    
    data = {'email': 'testemail@gmail.com', 'password': 'admin1600'}

    def test_valid_serializer(self, db):
        """Test valid login serializer data."""
        User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
        serializer = UserLoginSerializer(data=self.data)
        assert serializer.is_valid() == True


class TestPassowordChangeSerializer:
    
    data = {'old_password': 'admin1600', 'new_password1': 'admin160', 'new_password2': 'admin160'}
    url = reverse('users-api:password-change')

    def test_valid_serializer(self, db, api_factory):
        """Test valid serializer data."""
        # data is valid 
        user = User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
        request = api_factory.get(self.url)
        request.user = user
        serializer = PassowordChangeSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == True
        # old password is incorrect
        self.data['old_password'] = 'admin16'
        serializer = PassowordChangeSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == False
        assert serializer.errors['old_password'][0] == 'Password is incorrect.'
        # two passwords don't match
        self.data['old_password'] = 'admin1600'
        self.data['new_password2'] = 'admin16000'
        serializer = PassowordChangeSerializer(data=self.data, context={"request": request})
        assert serializer.is_valid() == False
        assert serializer.errors['new_password1'][0] == 'The two Passwords must match.'
        

class TestRequestPasswordResetEmailSerializer:

    data = {'email': 'testemail@gmail.com'}

    def test_valid_data(self, db):
        """Test valid serializer data."""
        User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
        serializer = RequestPasswordResetEmailSerializer(data=self.data)
        assert serializer.is_valid() == True
    
    def test_email_incorrect(self, db):
        """Test invalid email value data."""
        self.data['email'] = 'testemail0@gmail.com'
        User.objects.create_user(email='testemail@gmail.com', password='admin1600', is_verified=True)
        serializer = RequestPasswordResetEmailSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'Email is incorrect.'

    def test_account_inactive(self, db):
        """Test inactive account."""
        self.data['email'] = 'testemail@gmail.com'
        User.objects.create_user(email='testemail@gmail.com', password='admin1600')
        serializer = RequestPasswordResetEmailSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['email'][0] == 'Account is not active.'    
       

class TestResetPasswordSerializer:

    data = {'new_password1': 'admin160', 'new_password2': 'admin160'}

    def test_valid_data(self, new_user):
        """Test valid serializer data."""
        # valid data
        self.data['token'] = str(PasswordResetTokenGenerator().make_token(new_user))
        self.data['uidb64'] = urlsafe_base64_encode(smart_bytes(new_user.id))
        serializer = PasswordResetSerializer(data=self.data)
        assert serializer.is_valid() == True
        # two passwords don't match
        self.data['new_password2'] = 'admin16'
        serializer = PasswordResetSerializer(data=self.data)
        assert serializer.is_valid() == False
        assert serializer.errors['new_password1'][0] == 'The two Passwords must match.' 

    def test_invalid_token(self, new_user):
        """Test invalid token."""
        self.data['token'] = 'token'
        serializer = PasswordResetSerializer(data=self.data)
        assert serializer.is_valid() == False
