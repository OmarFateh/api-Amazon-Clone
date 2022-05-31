from django.contrib import admin

from .models import *


# models admin site registeration.
admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(AttributeValue) 
admin.site.register(ProductVariant)
admin.site.register(ProductVariantImage) 
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Review)
admin.site.register(Wishlist)