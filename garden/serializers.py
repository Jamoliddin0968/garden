# Garden,Product,Sell,SellItem,Order,OrderItem,Monthly,MonthlyItem,Expense,ExpenseItem,Storage
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
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

# buyurtma yaratish ------------------------------------------------

class OrderCreateSerializer(serializers.Serializer):
    class OrderItemCreateSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.FloatField()

    id=serializers.IntegerField(read_only=True)
    garden_id = serializers.IntegerField()
    date = serializers.DateField(read_only=True)
    items = OrderItemCreateSerializer(many=True)
    
    def validate(self, attrs):
        return super().validate(attrs)
    def create(self, validated_data):
        items = validated_data.pop('items',[])
        garden_id = validated_data.get('garden_id')
        objects=[]
        order=Order.objects.create(garden_id=garden_id)
        for item in items:
            obj = OrderItem(order=order)
            obj.product_id=item.get("product_id")
            obj.quantity=item.get("quantity")
            objects.append(obj)
        OrderItem.objects.bulk_create(objects)
        return order
# buyurtma list

class OrderSerializer(ModelSerializer):
    class OrderItemSerializer(ModelSerializer):
        product = ProductSerializer()
        class Meta:
            exclude = ('id','order')
            model = OrderItem

    garden=GardenSerializer()
    items = OrderItemSerializer(many=True)
    class Meta:
        fields=("garden","date","items")
        model=Order
# end the oredr model ------------------------------------------------

# oylik
class MonthlySerializer(ModelSerializer):
    class Meta:
        fields="__all__"
        model=Monthly

class LimitCreateSerializer(serializers.Serializer):
    class ItemSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        limit_quantity = serializers.FloatField(default=0)
        price = serializers.IntegerField()
        market_price = serializers.IntegerField()
    monthly_id = serializers.IntegerField()  
    garden_id = serializers.IntegerField()
    items = ItemSerializer(many=True)
    def create(self, validated_data):
        items = validated_data.pop('items',[])
        limit = Limit.objects.create(garden_id=garden_id,monthly_id=monthly_id)
        objects=[]
        for item in items:
            obj = LimitItem(limit_id=limit.id,**validated_data)
            objects.append(obj)
        LimitItem.objects.bulk_create(objects)
            
        return limit
    
# end 



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
