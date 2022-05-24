from django.urls import path

from .views import (RegisterMerchantAPIView, RegisterCustomerAPIView, RequestVerfiyEmailAPIView, VerfiyEmailAPIView, 
                    UserLoginAPIView, UserLogoutAPIView, PassowordChangeAPIView, RequestPasswordResetEmailAPIView, 
                    PasswordResetFormAPIView)


"""
CLIENT
BASE ENDPOINT /api/users/
"""

urlpatterns = [
    # Authentication
    path('register/merchant/', RegisterMerchantAPIView.as_view(), name='register-merchant'),
    path('register/customer/', RegisterCustomerAPIView.as_view(), name='register-customer'),
    path('account/activate/', RequestVerfiyEmailAPIView.as_view(), name='verfiy-email'),
    path('account/activate/<token>/', VerfiyEmailAPIView.as_view(), name='verfiy-email-confirm'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    # Token
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Password
    path('password/change/', PassowordChangeAPIView.as_view(), name='password-change'),
    path('password/reset/', RequestPasswordResetEmailAPIView.as_view(), name='password-reset'),
    # path('password/reset/<uidb64>/<token>/', PasswordResetTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('password/reset/complete/<token>/', PasswordResetFormAPIView.as_view(), name='password-reset-complete'),
]