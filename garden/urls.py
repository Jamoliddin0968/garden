from django.urls import include, path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('order/create/', OrderCreateAPIView.as_view()),
    path('get_current_monthly/', GetActiveMonthly.as_view()),
    path('create_new_monthly/', CreateNewMonthly.as_view()),
    path('close_current_monthly/', CloseActiveMonthly.as_view()),
    path('products/<int:garden_id>/', ProductGarden.as_view()),
    path('limit_create/', LimitCreateAPIView.as_view()),
    path('sell_create/', SellCreateAPIView.as_view()),
    path('expense_create/', ExpenseCreateAPIView.as_view()),
    path('gardens/', GardenViewSet.as_view())

]

router = routers.SimpleRouter()

# router.register(r'Garden', GardenViewSet)


# router.register(r'Expense', ExpenseViewSet)

router.register(r'Storage', StorageViewSet)
urlpatterns += router.urls
