from django.contrib import admin

# from mptt.admin import MPTTModelAdmin

from .models import Category


# models admin site registeration
admin.site.register(Category)