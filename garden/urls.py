from django.urls import include, path
from rest_framework import routers

from .views import *

urlpatterns = [
    path('order/create/', OrderCreateAPIView.as_view({"post": "post"})),
    path('get_current_monthly/', ActiveMonthly.as_view({"get": "get"})),
    path('create_new_monthly/',
         ActiveMonthly.as_view({"post": "create_new_monthly"})),
    path('close_current_monthly/',
         ActiveMonthly.as_view({"post": "close_active_monthly"})),
    path('products/<int:user_id>/', ProductGarden.as_view()),
    path('limit/create/', LimitViewSet.as_view({'post': 'post'})),
    path('sell_create/', SellCreateAPIView.as_view()),
    path('expense/create/', ExpenseViewSet.as_view({"post": "create"})),
    path('expense/all/', ExpenseViewSet.as_view({"get": "list"})),
    path('expense/<str:date>/', ExpenseViewSet.as_view({'get': 'retrieve'})),
    path('garden/all/', GardenViewSet.as_view({"get": "list"})),
    path('garden/monthly/<int:user_id>',
         GardenViewSet.as_view({"get": "retrieve"})),
    path('garden/check/<str:user_id>',
         GardenViewSet.as_view({"get": "get_by_tg_user_id"})),
    path('garden/detail/',
         GardenViewSet.as_view({"post": "get_by_phone_number"})),
    path('limit/', LimitViewSet.as_view({'get': 'get'})),
    path('get_hisob_factura/<int:user_id>',
         DocumentViewSet.as_view({'get': "hisob_factura"})),
    path('verify_order/<int:order_id>',
         OrderCreateAPIView.as_view({"get": "verify_order"}), name="verify_order"),
    path('cancel_order/<int:order_id>',
         OrderCreateAPIView.as_view({"get": "cancel_order"}), name="cancel_order"),
]

router = routers.SimpleRouter()
router.register(r'Storage', StorageViewSet)
urlpatterns += router.urls
