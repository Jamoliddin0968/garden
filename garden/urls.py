from django.urls import include, path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('order/create/', OrderCreateAPIView.as_view()),
    path('get_current_monthly/', GetActiveMonthly.as_view()),
    path('create_new_monthly/', CreateNewMonthly.as_view()),
    path('close_current_monthly/', CloseActiveMonthly.as_view()),
    path('products/<int:garden_id>/', ProductGarden.as_view()),
    path('limit/create/', LimitViewSet.as_view({'post': 'post'})),
    path('sell_create/', SellCreateAPIView.as_view()),
    path('expense/create/', ExpenseViewSet.as_view({"post": "create"})),
    path('expense/all/', ExpenseViewSet.as_view({"get": "list"})),
    path('expense/<str:date>/', ExpenseViewSet.as_view({'get': 'retrieve'})),
    path('garden/all/', GardenViewSet.as_view({"get": "list"})),
    path('garden/monthly/<int:garden_id>',
         GardenViewSet.as_view({"get": "retrieve"})),
    path('limit/', LimitViewSet.as_view({'get': 'get'}))
]

router = routers.SimpleRouter()
router.register(r'Storage', StorageViewSet)
urlpatterns += router.urls
