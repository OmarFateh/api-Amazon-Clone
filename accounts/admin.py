from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


# models admin site registeration. 
admin.site.register(User)
# Remove Group Model from admin.
admin.site.unregister(Group)
