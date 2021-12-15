import factory

from accounts.models import User


class CustomerUserFactory(factory.django.DjangoModelFactory):
    """ Create new customer user instance."""
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'C'
    is_verified = True


class MerchantUserFactory(factory.django.DjangoModelFactory):
    """Create new merchant user instance."""
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail1@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'M'
    is_verified = True


class AdminUserFactory(factory.django.DjangoModelFactory):
    """Create new admin user instance."""
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = 'testemail0@gmail.com'
    first_name = 'omar'
    last_name = 'fateh'
    password = 'admin1600'
    user_type = 'A'
    is_verified = True