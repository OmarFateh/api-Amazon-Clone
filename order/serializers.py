from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator


from product.mixins import TimestampMixin
from .models import Order, OrderItem, Coupon


###
# Order
###
class OrderItemSerializer(serializers.ModelSerializer, TimestampMixin):
    """Order item model serializer."""
    item_id = serializers.IntegerField(min_value=1, write_only=True, required=False)

    class Meta:
        model  = OrderItem
        fields = ["id", "item_id", "product_variant", "purchase_price", "discount_amount", "quantity"]

    def create(self, validated_data):
        """Create new order item."""
        order_id = self.context['order_id']
        order_item_obj = OrderItem.objects.create(**validated_data, order_id=order_id)
        return order_item_obj

        
class OrderSerializer(serializers.ModelSerializer, TimestampMixin):
    """Order model serializer."""
    order_items = OrderItemSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model  = Order
        fields = ["id", "order_items", "shipping_address", "payment", "coupon", "total_paid", "billing_status", "shipping_status"]

    def validate(self, data):
        """
        Validate that existing order item obj has id & the order has this item id, and has new item data to create new one.
        """
        is_update = self.context['is_update']
        items = data.get('order_items')
        if is_update:
            order_obj = self.context['order_obj']
            if items:
                for item in items:
                    # incorrect item id
                    if 'item_id' in item.keys() and item['item_id'] not in order_obj.order_items.values_list('id', flat=True):
                        raise serializers.ValidationError({"order_items": {"item_id": "This order does not have this item id."}})
                    #required fields
                    if 'item_id' not in item.keys():
                        keys_lst = ['product_variant', 'purchase_price', 'quantity']
                        for key in keys_lst:
                            if key not in item.keys():
                                raise serializers.ValidationError({"order_items": {key: "This field is required."}})        
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Create new order with order items as a nested serializer."""
        if 'order_items' in validated_data.keys():
            items = validated_data.pop('order_items')
            order_obj = Order.objects.create(**validated_data)
            for item in items:
                OrderItemSerializer.create(OrderItemSerializer(context={"order_id": order_obj.id}), validated_data=item)                           
        else:
            order_obj = Order.objects.create(**validated_data)
        return order_obj

    @transaction.atomic
    def update(self, instance, validated_data):
        """Update order & items of nested serializer."""
        if 'order_items' in validated_data.keys():
            items = validated_data.pop('order_items')
            for item in items:
                # update existing items
                if 'item_id' in item.keys():
                    item_obj = get_object_or_404(OrderItem, id=item['item_id'])
                    OrderItemSerializer.update(OrderItemSerializer(), instance=item_obj, validated_data=item)
                # create new ones
                else:
                    new_item_obj = OrderItemSerializer.create(OrderItemSerializer(context={"order_id": instance.id}), 
                                    validated_data=item)
        return super().update(instance, validated_data)


###
# Coupon
###
class CouponSerializer(serializers.ModelSerializer, TimestampMixin):
    """Coupon model serializer."""

    class Meta:
        model  = Coupon
        fields = ["id", "code", "valid_from", "valid_to", "discount_amount", "is_active"]
        # validators = [UniqueTogetherValidator(queryset=Coupon.objects.all(), fields=['code'])]

    # def validate_code(self, value):
    #     """Validate that code is unique."""
    #     is_create = self.context['is_create']
    #     error = False
    #     if is_create:
    #         if Coupon.objects.filter(code__iexact=value).exists():
    #             error = True
    #     else:
    #         coupon = self.context['coupon']
    #         if Coupon.objects.filter(code__iexact=value).exclude(code=coupon.code).exists():
    #             error = True
    #     if error:
    #         raise serializers.ValidationError("Coupon with this name already exists.")
    #     return value   

    def validate(self, data):
        """Validate that valid to date is greater than valid from."""
        valid_from = data.get('valid_from')
        valid_to = data.get('valid_to')
        if not valid_from:
            valid_from = self.instance.valid_from    
        if not valid_to:
            valid_to = self.instance.valid_to
        if valid_to < valid_from:
            raise serializers.ValidationError({"valid_from": "Valid from date should be earlier than valid to date."})
        return data     