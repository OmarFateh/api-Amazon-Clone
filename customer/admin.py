from django.contrib import admin

from .models import Customer, Address


# models admin site registeration. 
admin.site.register(Customer)
admin.site.register(Address)
