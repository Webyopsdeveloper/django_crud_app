from rest_framework import viewsets 
from .serializers import customer_serializer, category_serializer, order_serializer, orderitem_serializer, product_serializer 

from .models import Customer, Category, Order, OrderItem, Product 
# from .models import Category 
# from .serializers import category_serializer

class customer_viewset(viewsets.ModelViewSet):
    queryset= Customer.objects.all()
    serializer_class = customer_serializer 
class category_viewset(viewsets.ModelViewSet):
    queryset= Category.objects.all()
    serializer_class = category_serializer 
class order_viewset(viewsets.ModelViewSet):
    queryset= Order.objects.all()
    serializer_class = order_serializer 
class orderitem_viewset(viewsets.ModelViewSet):
    queryset= OrderItem.objects.all()
    serializer_class = orderitem_serializer 
class product_viewset(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class = product_serializer 