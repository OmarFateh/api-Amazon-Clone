from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .utils import send_activation_reset_email


class UserSerializer(serializers.ModelSerializer):
    """ A serializer for user registeration."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {"password": {'write_only': True}}

    def validate_password(self, value):
        """Validate that password meet django auth validators."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({'password':e})
        return value      

    def validate_email(self, value):
        """Validate the uniqueness of email."""
        # check if the email has already been used.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email':"An account with this Email already exists."})
        return value

    def create(self, validated_data):
        """Create and send activation email to new user."""
        request = self.context['request']
        user_type = self.context['user_type']  
        user_obj = User.objects.create_user(user_type=user_type, **validated_data)
        # send activation email
        send_activation_reset_email(request, user_obj, is_activation=True)                
        return user_obj


class EmailVerificationSerializer(serializers.ModelSerializer):
    """A serializer for email verification token."""
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class RequestEmailVerificationEmailSerializer(serializers.ModelSerializer):
    """Request Email verification email serializer."""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, value):
        """Validate entered data."""
        email = value
        # check if the entered email is correct.
        users_qs = User.objects.filter(email__iexact=email)
        if not users_qs.exists():
            raise serializers.ValidationError("Email is incorrect.")  
        if users_qs.filter(is_verified=True).exists():
            raise serializers.ValidationError("Account is already activated.")
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    """A serializer for user login."""
    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        extra_kwargs = {"password": {'write_only': True}}

    def get_token(self, obj):
        user = User.objects.get(email=obj['email'])
        refresh = RefreshToken.for_user(user)
        response = {'refresh': str(refresh), 'access': str(
            refresh.access_token), }
        return response

    def validate(self, data):
        """Validate entered data."""
        email = data.get("email", None)
        password = data["password"]
        # check if the entered email and password are correct.
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:            
            raise AuthenticationFailed('Account is not activated')
        return data


class LogoutSerializer(serializers.Serializer):
    """A serializer for user logout."""
    refresh_token = serializers.CharField(label='Refresh Token')

    def validate(self, data):
        """Validate entered data."""
        refresh_token = data.get("refresh_token", None)
        # check if the entered token is valid and add it to blacklist.
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError as e:
            raise serializers.ValidationError("Token is invalid or expired.")
        return data

# class LogoutSerializer(serializers.Serializer):
#     """
#     """
#     refresh = serializers.CharField()

#     default_error_message = {
#         'bad_token': ('Token is expired or invalid')
#     }

#     def validate(self, data):
#         self.token = data['refresh']
#         return data

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token).blacklist()
#         except TokenError:
#             self.fail(self.default_error_messages)


class PassowordChangeSerializer(serializers.ModelSerializer):
    """A serializer for password change."""
    old_password = serializers.CharField(label='Old Password', write_only=True)
    new_password1 = serializers.CharField(
        label='New Password', write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1']

    def validate_old_password(self, value):
        """Validate old password."""
        request = self.context['request']
        # check if the password is correct
        if not request.user.check_password(value):
            raise serializers.ValidationError("Password is incorrect.")
        return value

    def update(self, instance, validated_data):
        """Update user's password."""
        password = validated_data['new_password1']
        instance.set_password(password)
        instance.save()
        return validated_data


class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    """Request Password reset email serializer."""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate_email(self, value):
        """Validate email."""
        email = value
        # check if the entered email is correct.
        users_qs = User.objects.filter(email__iexact=email)
        if not users_qs.exists():
            raise serializers.ValidationError("Email is incorrect.")  
        if not users_qs.filter(is_verified=True).exists():
            raise serializers.ValidationError("Account is not active.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """Password reset serializer."""
    new_password1 = serializers.CharField(
        label='New Password', write_only=True)
    token = serializers.CharField(label='Token', write_only=True)
    uidb64 = serializers.CharField(label='UIDB64', write_only=True)

    class Meta:
        fields = ['new_password1', 'token', 'uidb64']

    def validate(self, data):
        """Validate entered data."""
        try:
            password = data.get("new_password1")
            token = data.get("token")
            uidb64 = data.get("uidb64")
            # get user by id.
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=user_id)
            # check if the token is valid.
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid.', 401)
            # set new password
            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed('The reset link is invalid.', 401)
        return data