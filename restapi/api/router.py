from rest_framework import routers 
from .views import customer_viewset, category_viewset, product_viewset, order_viewset, orderitem_viewset 
# from .views import category_viewset

router = routers.DefaultRouter()
router.register('Customer', customer_viewset)
router.register('Product', product_viewset)
router.register('Order', order_viewset)
router.register('OrderItem', orderitem_viewset)
router.register('Category', category_viewset)
