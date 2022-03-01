from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    billing_profile = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    billing_address = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'billing_profile',
            'order_id',
            'shipping_address',
            'billing_address',
            'shipping_address_final',
            'billing_address_final',
            'cart',
            'status',
            'shipping_total',
            'total',
            'active',
            'updated',
            'timestamp'
        ]
