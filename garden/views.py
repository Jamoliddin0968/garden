from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,GenericAPIView
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response

from rest_framework import status
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

# buyurtma
class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    @extend_schema(
        request=OrderCreateSerializer,
        responses={
        status.HTTP_201_CREATED: OrderSerializer,
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"message": {"type": "string","example":"Limitdan o'tib ketdi"}}}
    },
    )
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer_response = OrderSerializer(order)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)

# class OrderListAPIView(RetrieveAPIView):
#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()

# buyurtma

class LimitViewSet(viewsets.ModelViewSet):
    serializer_class = LimitCreateSerializer
    queryset = Limit.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LimitCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        limit=serializer.save()
        serializer = LimitSerializer(limit)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()


class ExpenseItemViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseItemSerializer
    queryset = ExpenseItem.objects.all()

class GetActiveMonthly(GenericAPIView):
    model=Monthly
    serializer_class=MonthlySerializer
    
    def get(self,request):
        obj=Monthly.objects.filter(is_active=True).order_by('-id').last()
        if obj:
            serializer=MonthlySerializer(obj)
        return Response(serializer.data,status=200)
    
class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()