from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title = "Amazon Clone API",
        default_version = "V1",
        description = "Test Description",
        terms_of_service = "https://www.amazonclone.com/policies/terms/",
        contact = openapi.Contact(email="contact@amazonclone.local"),
        license = openapi.License(name="Test License"),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Swagger 
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # API Endpoints
    path('api/users/', include(('accounts.urls', 'accounts'), namespace='users-api')),
    path('api/categories/', include(('category.urls', 'category'), namespace='category-api')),
    path('api/brands/', include(('brand.urls', 'brand'), namespace='brand-api')),
    path('api/customers/', include(('customer.urls', 'customer'), namespace='customer-api')),
    path('api/merchants/', include(('merchant.urls', 'merchant'), namespace='merchant-api')),
    path('api/products/', include(('product.urls', 'product'), namespace='product-api')),
    path('api/orders/', include(('order.urls', 'order'), namespace='order-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)