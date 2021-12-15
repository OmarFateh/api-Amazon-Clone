from rest_framework import serializers

from accounts.serializers import UserSerializer
from accounts.mixins import UserUpdateMixins
from .models import Merchant
from accounts.models import User


class MerchantCreateSerializer(serializers.ModelSerializer):
    """A serializer to create new merchant."""
    user = UserSerializer(required=True)

    class Meta:
        model = Merchant
        fields = ['id', 'user', 'company_name', 'gst_detail']

    def create(self, validated_data):
        """
        Create user obj with user nested serializer.
        Assign data values to user merchant and save it.
        """
        request = self.context['request']
        user_data = validated_data['user']
        user_obj = UserSerializer.create(UserSerializer(context={"user_type": "M", "request": request}), 
                                validated_data=user_data)
        # assign keys & value to user merchant.
        for key, value in validated_data.items():
            if key != 'user':
                setattr(user_obj.merchant, key, value) 
        user_obj.merchant.save()
        return validated_data


class MerchantDetailSerializer(serializers.ModelSerializer, UserUpdateMixins):
    """A serializer to display or update merchant's data."""
    class Meta:
        model = Merchant
        fields = ['id', 'first_name', 'last_name', 'email', 'company_name', 'gst_detail']
        # extra_kwargs = {'specialization': {'required': False}, 'info': {'required': False}}

    def update(self, instance, validated_data):
        """
        Update user obj with user nested serializer.
        Assign data values to user merchant and save it.
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