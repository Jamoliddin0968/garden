# Garden,Product,Sell,SellItem,Order,OrderItem,Monthly,MonthlyItem,Expense,ExpenseItem,Storage
from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import *


def get_current_monthly() -> Monthly:
    obj = Monthly.objects.filter(is_active=True).first()
    if not obj:
        raise ValidationError("Aktiv oylik obyekt mavjud emas")
    return obj

# oylik


class MonthlySerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Monthly


class TgAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    user_id = serializers.CharField(max_length=10)

    def validate(self, attrs):

        data = super().validate(attrs)
        phone_number = data.get('phone_number')
        if not phone_number.startswith('+'):
            phone_number = '+'+phone_number
            data["phone_number"] = phone_number
        return data


class ProductGardenParametr(serializers.Serializer):
    monthly_id = serializers.IntegerField()
    garden_id = serializers.IntegerField()


class GardenSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Garden


class ProductSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product


class SellCreateSerializer(serializers.Serializer):
    class _SellCreateItemSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.FloatField()
        # price = serializers.IntegerField()

    garden_id = serializers.IntegerField()
    monthly_id = serializers.IntegerField(read_only=True)
    items = _SellCreateItemSerializer(many=True)

    def create(self, validated_data):
        monthly_id = get_current_monthly().id
        garden_id = validated_data.get('garden_id')
        items = validated_data.pop('items')
        sell_object = Sell.objects.create(
            monthly_id=monthly_id, garden_id=garden_id)
        objects = []
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            price = 0
            temp = LimitItem.objects.filter(
                Q(limit__monthly__id=monthly_id) & Q(product_id=product_id)).first()
            if temp:
                price = temp.price
            obj = SellItem(
                sell=sell_object, price=price, product_id=product_id, quantity=quantity)
            objects.append(obj)
        SellItem.objects.bulk_create(objects)
        for obj in objects:
            product_id, quantity = obj.product_id, obj.quantity
            product, _ = Storage.objects.get_or_create(product_id=product_id)
            product.balance -= quantity
            product.save()
        return sell_object


class SellSerializer(ModelSerializer):
    class _SellItemSerializer(ModelSerializer):
        product = ProductSerializer()
        quantity = serializers.FloatField()
        price = serializers.IntegerField()

        class Meta:
            fields = "__all__"
            model = SellItem

    garden = GardenSerializer()
    monthly = MonthlySerializer()
    items = _SellItemSerializer(many=True, source='sellitem_set')

    class Meta:
        fields = "__all__"
        model = Sell


class OrderCreateSerializer(serializers.Serializer):
    class _OrderItemCreateSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.FloatField()
    monthly_id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    date = serializers.DateField(read_only=True)
    items = _OrderItemCreateSerializer(many=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        items = data.get('items', [])
        monthly_id = get_current_monthly().id
        garden_id = get_object_or_404(
            Garden, tg_user_id=data.get('user_id')).id
        limit = Limit.objects.filter(
            monthly_id=monthly_id, garden_id=garden_id).first()
        if not limit:
            raise ValidationError(
                {"message": "Sizga hali limit belgilanmagan"})
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not LimitItem.objects.filter(limit=limit, product_id=product_id, remaining_quantity__gte=quantity).exists():
                raise ValidationError(
                    {"message": "limitdan ortib ketti", "product_id": product_id})

        return data

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        user_id = validated_data.get('user_id')
        garden = get_object_or_404(Garden, tg_user_id=user_id)
        objects = []
        monthly_id = get_current_monthly().id
        order = Order.objects.create(
            garden=garden, monthly_id=monthly_id)
        limit = Limit.objects.filter(
            garden=garden, monthly_id=monthly_id).first()
        for item in items:
            obj = OrderItem(order=order)
            obj.product_id = item.get("product_id")
            obj.quantity = item.get("quantity")
            product = LimitItem.objects.filter(
                limit=limit, product_id=obj.product_id)
            product.remaining_quantity = product.remaining_quantity-obj.quantity
            product.save()
            objects.append(obj)
        OrderItem.objects.bulk_create(objects)
        return order


class OrderSerializer(ModelSerializer):
    class _OrderItemSerializer(ModelSerializer):
        product = ProductSerializer()

        class Meta:
            exclude = ('id', 'order')
            model = OrderItem
    monthly = MonthlySerializer()
    garden = GardenSerializer()
    items = _OrderItemSerializer(many=True)

    class Meta:
        fields = ("garden", "date", "items", "monthly")
        model = Order


class LimitCreateSerializer(serializers.Serializer):
    class _ItemCreateSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        limit_quantity = serializers.FloatField(default=0)
        remaining_quantity = serializers.FloatField(read_only=True)
        price = serializers.IntegerField()
        market_price = serializers.IntegerField()
    monthly_id = serializers.IntegerField(read_only=True)
    garden_id = serializers.IntegerField()
    items = _ItemCreateSerializer(many=True)

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        monthly_id = get_current_monthly().id
        limit, _ = Limit.objects.get_or_create(
            garden_id=validated_data.get('garden_id'), monthly_id=monthly_id)
        objects = []
        for item in items:
            obj = LimitItem(limit_id=limit.id, **item)
            obj.remaining_quantity = obj.limit_quantity
            objects.append(obj)
        LimitItem.objects.bulk_create(objects)

        return limit


class LimitSerializer(ModelSerializer):
    class _ItemSerializer(ModelSerializer):
        product = ProductSerializer()

        class Meta:
            exclude = ("id",)
            model = LimitItem
    monthly = MonthlySerializer()
    garden = GardenSerializer()
    items = _ItemSerializer(many=True, source='limititem_set')

    class Meta:
        exclude = ('id',)
        model = Limit


class ExpenseSerializer(ModelSerializer):
    class _ExpenseItemSerializer(ModelSerializer):
        class Meta:
            fields = "__all__"
            model = ExpenseItem
    items = _ExpenseItemSerializer(many=True, source='expenseitem_set')

    class Meta:
        fields = "__all__"
        model = Expense


class ExpenseCreateSerializer(serializers.Serializer):
    class _ExpenseItemCreateSerializer(serializers.Serializer):
        expense = serializers.IntegerField(read_only=True)
        product_id = serializers.IntegerField()
        quantity = serializers.FloatField()
        price = serializers.IntegerField(default=0)
        amount = serializers.IntegerField(read_only=True)
    items = _ExpenseItemCreateSerializer(many=True)

    def create(self, validated_data):
        monthly_id = get_current_monthly().id
        date = datetime.now()
        expense, _ = Expense.objects.get_or_create(
            monthly_id=monthly_id, date=date)
        items = validated_data.pop('items', [])
        objects = []
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            price = item.get('price')
            amount = quantity*price
            obj = ExpenseItem(expense=expense, product_id=product_id,
                              quantity=quantity, price=price, amount=amount)
            objects.append(obj)
        ExpenseItem.objects.bulk_create(objects)
        for obj in objects:
            product_id, quantity = obj.product_id, obj.quantity
            product, _ = Storage.objects.get_or_create(product_id=product_id)
            product.balance += quantity
            product.save()
        return expense


class StorageSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Storage


class DailyExpence(ModelSerializer):
    class _DailyExpenseItemSerializer(ModelSerializer):
        class Meta:
            fields = "__all__"
            model = ExpenseItem
    items = _DailyExpenseItemSerializer(many=True, source='expenseitem_set')

    class Meta:
        fields = "__all__"
        model = Expense


class LimitItemSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = LimitItem


class LimitListSerializer(ModelSerializer):
    monthly = MonthlySerializer()
    items = LimitItemSerializer(many=True, source='limititem_set')

    class Meta:
        fields = "__all__"
        model = Limit


class MontlyLimitSerializer(ModelSerializer):
    items = LimitListSerializer(many=True, source="limit_set")

    class Meta:
        model = Monthly
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        products = Product.objects.all()
        gardens = Garden.objects.all()
        product_serializers = ProductSerializer(products, many=True).data
        garden_serializer = GardenSerializer(gardens, many=True).data
        additional_data = {"products": product_serializers,
                           'gardens': garden_serializer}
        data.update(additional_data)
        return data


class MontlyExpenseSerializer(ModelSerializer):
    items = DailyExpence(many=True, source="expense_set")

    class Meta:
        model = Monthly
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        products = Product.objects.all()
        product_serializers = ProductSerializer(products, many=True).data
        additional_data = {"products": product_serializers, }
        data.update(additional_data)
        return data


class MonthlyGardenSerializers(serializers.Serializer):
    class SingleLimitSerializer(serializers.ModelSerializer):
        class Meta:
            exclude = ("id",)
            model = Limit
    monthly = MonthlySerializer()
    garden = GardenSerializer()
    products = ProductSerializer(many=True)
    limit = SingleLimitSerializer()
    limit_items = LimitItemSerializer(many=True)
