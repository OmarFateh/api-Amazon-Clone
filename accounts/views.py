from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import jwt
from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from merchant.models import Merchant
from merchant.serializers import MerchantCreateSerializer
from customer.models import Customer
from customer.serializers import CustomerCreateSerializer
from .models import User
from .utils import send_activation_reset_email
from .permissions import AnonPermissionOnly
from .serializers import (EmailVerificationSerializer, 
                        RequestEmailVerificationEmailSerializer, UserLoginSerializer, 
                        RequestPasswordResetEmailSerializer, LogoutSerializer,
                        PassowordChangeSerializer, PasswordResetSerializer)


class RegisterMerchantAPIView(generics.CreateAPIView):
    """Merchant registeration and profile creation API view."""
    permission_classes = [AnonPermissionOnly]
    queryset = Merchant.objects.all()
    serializer_class = MerchantCreateSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class RegisterCustomerAPIView(generics.CreateAPIView):
    """Customer registeration and profile creation API view."""
    permission_classes = [AnonPermissionOnly]
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class RequestVerfiyEmailAPIView(APIView):
    """Request email verification API view."""    
    def post(self, request, *args, **kwargs):
        """Override the post method and request verifiy email mail."""
        serializer = RequestEmailVerificationEmailSerializer(
            data=request.data, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            # send email to user with email verification link.
            user = User.objects.get(email=request.data["email"])
            send_activation_reset_email(request, user, is_activation=True)
            return Response({"success": "We have sent you an email to verifiy your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerfiyEmailAPIView(generics.GenericAPIView):
    """Take token, and verify and activate account."""
    def get(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"success": "You email was verfied successfully"}, status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"error": "Activation Expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier: 
            return Response({"error": "Token is invalid, please request a new one."}, 
                            status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.GenericAPIView):
    """User login API view."""
    permission_classes = [AnonPermissionOnly]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(generics.GenericAPIView):
    """User logout API view."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PassowordChangeAPIView(generics.UpdateAPIView):
    """User profile update API view."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PassowordChangeSerializer

    def update(self, request, *args, **kwargs):
        """Override the update method and update user's password."""
        serializer = PassowordChangeSerializer(
            request.user, data=request.data, partial=True, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"success": "Your password was changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmailAPIView(APIView):
    """Request password reset email API view."""

    def post(self, request, *args, **kwargs):
        """Override the post method and request password reset email."""
        serializer = RequestPasswordResetEmailSerializer(
            data=request.data, context={"request": self.request})
        if serializer.is_valid(raise_exception=True):
            # send email to user with reset password link.
            user = User.objects.get(email=request.data["email"])
            send_activation_reset_email(request, user, is_reset=True)
            return Response({"success": "We have sent you an email to reset your password."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetTokenCheckAPIView(APIView):
    """Password reset token check API view."""

    def get(self, request, uidb64, token, *args, **kwargs):
        """Check if the token is valid, and return it and uidb64."""
        try:
            # decode the user's id and get the user by id.
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            # check if the token is valid.
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is invalid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"success": "Credintials are Valid", "uidb64": uidb64, "token": token}, status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({"error": "Token is invalid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetFormAPIView(generics.GenericAPIView):
    """Password reset form API view."""
    serializer_class = PasswordResetSerializer

    def patch(self, request, *args, **kwargs):
        """Override the patch method and reset user's password."""
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"success": "Your password was changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)