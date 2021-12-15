from django.dispatch import receiver
from django.db.models.signals import post_save

from customer.models import Customer
from merchant.models import Merchant
from useradmin.models import UserAdmin
from .models import User


@receiver(post_save, sender=User)     
def create_user_profile(sender, instance, created, **kwargs):
    """Create an empty profile for each user type once the user is added."""
    if created:
        if instance.user_type == 'A':
            UserAdmin.objects.create(user=instance)
        elif instance.user_type == 'M':   
            Merchant.objects.create(user=instance)
        elif instance.user_type == 'C':    
            Customer.objects.create(user=instance) 