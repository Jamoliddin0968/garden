from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,GenericAPIView
from .models import *
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import ValidationError,ParseError
from rest_framework.views import APIView
MONTHS=['Yanvar','Fevral','Mart','Aprel','May','Iyun','Iyul','Avgust','Sentyabr','Oktyabr','Noyabr','Dekabr']

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
    serializer_class=Monthly
    model=Monthly
    @extend_schema(
        summary="Hozirgi aktiv oylikni olish",
        description="Hozirigi aktiv oylik hisobotni olish",
        tags=["monthly"],
        request=None,
        responses={status.HTTP_201_CREATED: MonthlySerializer,}
    )
    def get(self,request):
        obj=Monthly.objects.filter(is_active=True).order_by('-id').last()
        if obj:
            serializer=MonthlySerializer(obj)
        return Response(serializer.data,status=200)
    
class CloseActiveMonthly(GenericAPIView):
    serializer_class=Monthly
    model=Monthly
    @extend_schema(
        summary="Hozirgi aktiv oylikni yopish",
        description="Hozirigi aktiv oylik hisobotni yopish",
        tags=["monthly"],
        request=None,
        responses={status.HTTP_200_OK:{"type": "object", "properties": {"message":{"type":"string","example":"OK"}}}}
    )
    def post(self,request):
        obj=Monthly.objects.filter(is_active=True).update(is_active=False)
        return Response({"message":"OK"},status=200)

class CreateNewMonthly(GenericAPIView):
    serializer_class=MonthlySerializer
    model=Monthly
    @extend_schema(
        summary="Yangi oylik ni yaratish",
        description="Shunchaki post zapros jo'natin va yangi obyektni olasiz",
        tags=["monthly"],
        request=None,
        responses={status.HTTP_201_CREATED: MonthlySerializer,
                   status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"message":{"type":"string","example":"Hozir aktiv oylik mavjud avval aktivlikni o'chiring"}}}
                   }
    
    )
    def post(self,request):
        if Monthly.objects.filter(is_active=True).exists():
            return Response({"message":"Hozir aktiv oylik mavjud avval aktivlikni o'chiring"},status=status.HTTP_400_BAD_REQUEST)
        current_month_number = datetime.now().month
        current_year=datetime.now().year
        month_name=MONTHS[current_month_number-1]
        obj=Monthly.objects.create(month=month_name,year=current_year)
        serializer = MonthlySerializer(obj)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()