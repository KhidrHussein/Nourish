from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, Payment, NewsletterSubscription, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    email = serializers.EmailField()