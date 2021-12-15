import factory

from useradmin.models import UserAdmin
from accounts.tests.factories import AdminUserFactory


class AdminFactory(factory.django.DjangoModelFactory):
    """Create new admin instance."""
    class Meta:
        model = UserAdmin
        django_get_or_create = ('user',)

    user = factory.SubFactory(AdminUserFactory)