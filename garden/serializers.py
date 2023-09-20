# Garden,Product,Sell,SellItem,Order,OrderItem,Monthly,MonthlyItem,Expense,ExpenseItem,Storage
from rest_framework.serializers import ModelSerializer
from .models import *

class GardenSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Garden
        
class ProductSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Product


class SellSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Sell


class SellItemSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=SellItem


class OrderSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Order


class OrderItemSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=OrderItem


class MonthlySerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Monthly


class MonthlyItemSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=MonthlyItem


class ExpenseSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Expense


class ExpenseItemSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=ExpenseItem


class StorageSerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Storage
