from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class GardenViewSet(viewsets.ModelViewSet):
    serializer_class = GardenSerializer
    queryset = Garden.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class SellViewSet(viewsets.ModelViewSet):
    serializer_class = SellSerializer
    queryset = Sell.objects.all()


class SellItemViewSet(viewsets.ModelViewSet):
    serializer_class = SellItemSerializer
    queryset = SellItem.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class MonthlyViewSet(viewsets.ModelViewSet):
    serializer_class = MonthlySerializer
    queryset = Monthly.objects.all()


class MonthlyItemViewSet(viewsets.ModelViewSet):
    serializer_class = MonthlyItemSerializer
    queryset = MonthlyItem.objects.all()


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()


class ExpenseItemViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseItemSerializer
    queryset = ExpenseItem.objects.all()


class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()