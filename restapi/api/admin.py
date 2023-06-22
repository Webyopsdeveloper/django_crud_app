from django.contrib import admin

# Register your models here.
from .models import Customer, Order, OrderItem, Product, Category 
# from .models import Category

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Category)