from rest_framework import serializers 
from .models import Category, Order, OrderItem, Customer, Product
# from .models import Category

class category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'

class order_serializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = '__all__'

class orderitem_serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem 
        fields = '__all__'

class customer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer 
        fields = '__all__'

class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = '__all__'
