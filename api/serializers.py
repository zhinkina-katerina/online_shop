from rest_framework import serializers

from orders.models import Order
from orders.product_order_model import ProductsInOrder
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductsInOrderSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = ProductsInOrder
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    products = ProductsInOrderSerializer(many=True, source='productsinorder_set')

    class Meta:
        model = Order
        fields = ('date_creation', 'status', 'total_price', 'products')


class CartHexSerializer(serializers.Serializer):
    cart_hex = serializers.CharField(max_length=255)


class CartSerializer(serializers.Serializer):
    product_title = serializers.CharField(max_length=255)
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
