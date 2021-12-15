from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password


class UserManager(BaseUserManager):
    """Custom user model manager."""
    def validate_email_address(self, email):
        """Take email and check if it's a valid email."""
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('You must provide a valid email address.')
            
    def validate_password(self, password):
        """Take password and check if it's a valid password."""
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValueError(e)

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if email:
            # Normalize the email address by lowercasing the domain part of it.
            email = self.normalize_email(email)
            self.validate_email_address(email)
        else:    
            raise ValueError('Users must have an email address')
        if password:
            self.validate_password(password)
        else:
            raise ValueError('Users must have a password')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """Take email and password, and create superuser."""
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True, user_type="A")    
        return user


class User(AbstractUser):
    """
    Custom user model where email is the unique identifiers
    for authentication instead of username.
    """
    TYPES_CHOICES = (
        ('A', 'Admin'),
        ('M', 'Merchant'),
        ('C', 'Customer'),
    )

    username = None
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=1, choices=TYPES_CHOICES, default='C')
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # USERNAME_FIELD and password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email

    def email_user(self, subject, message):
        send_mail(
            subject, # subject  
            message, # message
            settings.EMAIL_HOST_USER, # from email
            [self.email,], # to email list
            fail_silently=False,
        )
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_admin(self):
        """Return True if User is Admin, else False"""
        return self.user_type == 'A'    

    def is_merchant(self):
        """Return True if User is Merchant, else False"""
        return self.user_type == 'M'

    def is_customer(self):
        """Return True if User is Customer, else False"""
        return self.user_type == 'C'