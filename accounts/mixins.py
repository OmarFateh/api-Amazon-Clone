from rest_framework import serializers

from .models import User


class UserUpdateMixins(serializers.Serializer):
    """A mixin serializer to display or update user's data."""
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    def validate_email(self, value):
        """Validate email."""
        request = self.context['request']
        email = value
        # check if the email has already been used.
        if User.objects.filter(email=email).exclude(email=request.user.email).exists():
            raise serializers.ValidationError("An account with this Email already exists.")
        return value    