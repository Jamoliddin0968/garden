from django.urls import path , include

from .views import *
from rest_framework import routers

urlpatterns = [
    path('order/create/',OrderCreateAPIView.as_view()),
    path('get_current_monthly/',GetActiveMonthly.as_view())
]

router = routers.SimpleRouter()

router.register(r'Garden', GardenViewSet)


router.register(r'Product', ProductViewSet)


router.register(r'Sell', SellViewSet)


router.register(r'SellItem', SellItemViewSet)




router.register(r'Limit', LimitViewSet)

router.register(r'Expense', ExpenseViewSet)


router.register(r'ExpenseItem', ExpenseItemViewSet)


router.register(r'Storage', StorageViewSet)
urlpatterns += router.urls