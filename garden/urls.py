from django.urls import path , include

from .views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'Garden', GardenViewSet)


router.register(r'Product', ProductViewSet)


router.register(r'Sell', SellViewSet)


router.register(r'SellItem', SellItemViewSet)


router.register(r'Order', OrderViewSet)


router.register(r'OrderItem', OrderItemViewSet)


router.register(r'Monthly', MonthlyViewSet)


router.register(r'MonthlyItem', MonthlyItemViewSet)


router.register(r'Expense', ExpenseViewSet)


router.register(r'ExpenseItem', ExpenseItemViewSet)


router.register(r'Storage', StorageViewSet)
urlpatterns = router.urls