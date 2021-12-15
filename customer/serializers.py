from rest_framework import serializers

from product.mixins import TimestampMixin
from accounts.serializers import UserSerializer
from accounts.mixins import UserUpdateMixins
from .models import Customer, Address, Payment


class CustomerCreateSerializer(serializers.ModelSerializer):
    """A serializer to create new customer."""
    user = UserSerializer(required=True)

    class Meta:
        model = Customer
        fields = ['id', 'user']

    def create(self, validated_data):
        """
        Create user obj with user nested serializer.
        Assign data values to user customer and save it.
        """
        request = self.context['request']
        user_data = validated_data['user']
        user_obj = UserSerializer.create(UserSerializer(context={"user_type": "C", "request": request}), 
                                validated_data=user_data)
        # assign keys & value to user customer.
        for key, value in validated_data.items():
            if key != 'user':
                setattr(user_obj.customer, key, value) 
        user_obj.customer.save()
        return validated_data


class CustomerDetailSerializer(serializers.ModelSerializer, UserUpdateMixins):
    """A serializer to display or update customer's data."""
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        """
        Update user obj with user nested serializer.
        Assign data values to user customer and save it.
        """
        user_dict = validated_data['user']
        if user_dict:
            user_obj = instance.user
            for key, value in user_dict.items():
                setattr(user_obj, key, value)
            user_obj.save()
            validated_data["user"] = user_obj
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance 


# class CustomerSerializer(serializers.ModelSerializer):
#     """A serializer for customer data."""
#     first_name = serializers.CharField(source='user.first_name')
#     last_name = serializers.CharField(source='user.last_name')
#     email = serializers.EmailField(source='user.email')
#     class Meta:
#         model = Customer
#         fields = ['first_name', 'last_name', 'email']


class AddressSerializer(serializers.ModelSerializer, TimestampMixin):
    """Customer Address model serializer."""
    class Meta:
        model  = Address
        fields = ['id', 'uuid4', 'full_name', 'phone', 'address_line1', 'address_line2', 
                'country', 'city', 'postal_code', 'is_default', 'updated_at', 'created_at']
        read_only_fields = ['uuid4']


class PaymentSerializer(serializers.ModelSerializer, TimestampMixin):
    """Customer Payment model serializer."""
    class Meta:
        model  = Payment
        fields = ['id', 'uuid4', 'payment_type', 'provider', 'account_no', 'expiry_date', 
                'is_default', 'updated_at', 'created_at']
        read_only_fields = ['uuid4']        