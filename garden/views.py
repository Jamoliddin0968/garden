from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     ListAPIView, RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import (ExpenseCreateSerializer, ExpenseSerializer,
                          GardenSerializer, LimitCreateSerializer,
                          LimitSerializer, MonthlySerializer,
                          OrderCreateSerializer, OrderSerializer,
                          ProductSerializer, SellCreateSerializer,
                          SellSerializer, StorageSerializer,
                          get_current_monthly)

MONTHS = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
          'Iyul', 'Avgust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr']


class GardenViewSet(ListAPIView):
    serializer_class = GardenSerializer
    queryset = Garden.objects.all()


class ProductGarden(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, garden_id):
        monthly_id = get_current_monthly().id
        limits = Limit.objects.filter(
            Q(monthly_id=monthly_id) & Q(garden_id=garden_id)).first()
        if not limits:
            raise ValidationError(
                {"message": "Sizga hali limit belgilanmagan"})
        serializer = LimitSerializer(limits)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @extend_schema(
        summary="Buyurtma yaratish",
        description="Buyurtma yaratish",
        request=OrderCreateSerializer,
        responses={
            status.HTTP_201_CREATED: OrderSerializer,
            status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {
                "message": {"type": "string", "example": "Limitdan o'tib ketdi"}}}
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer_response = OrderSerializer(order)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)


class LimitCreateAPIView(CreateAPIView):
    serializer_class = LimitCreateSerializer
    queryset = Limit.objects.all()

    @extend_schema(
        summary="Limit jadvaliga ma'lumot qo'shish",
        description="Limit jadvaliga ma'lumot qo'shish: bu yerda bitta bog'cha uchun itemlar kiritladi",
        tags=["Limit"],
        request=LimitCreateSerializer,
        responses={status.HTTP_201_CREATED: LimitSerializer, }
    )
    def post(self, request, *args, **kwargs):
        serializer = LimitCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        limit = serializer.save()
        serializer = LimitSerializer(limit)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class ExpenseViewSet(viewsets.ModelViewSet):
#     serializer_class = ExpenseSerializer
#     queryset = Expense.objects.all()


class GetActiveMonthly(GenericAPIView):
    serializer_class = Monthly
    model = Monthly

    @extend_schema(
        summary="Hozirgi aktiv oylikni olish",
        description="Hozirigi aktiv oylik hisobotni olish",
        tags=["monthly"],
        request=None,
        responses={status.HTTP_201_CREATED: MonthlySerializer, }
    )
    def get(self, request):
        obj = Monthly.objects.filter(is_active=True).order_by('-id').last()
        if obj:
            serializer = MonthlySerializer(obj)
        return Response(serializer.data, status=200)


class CloseActiveMonthly(GenericAPIView):
    serializer_class = Monthly
    model = Monthly

    @extend_schema(
        summary="Hozirgi aktiv oylikni yopish",
        description="Hozirigi aktiv oylik hisobotni yopish",
        tags=["monthly"],
        request=None,
        responses={status.HTTP_200_OK: {"type": "object", "properties": {
            "message": {"type": "string", "example": "OK"}}}}
    )
    def post(self, request):
        obj = Monthly.objects.filter(is_active=True).update(is_active=False)
        return Response({"message": "OK"}, status=200)


class CreateNewMonthly(GenericAPIView):
    serializer_class = MonthlySerializer
    model = Monthly

    @extend_schema(
        summary="Yangi oylik ni yaratish",
        description="Shunchaki post zapros jo'natin va yangi obyektni olasiz",
        tags=["monthly"],
        request=None,
        responses={status.HTTP_201_CREATED: MonthlySerializer,
                   status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"message": {
                       "type": "string", "example": "Hozir aktiv oylik mavjud avval aktivlikni o'chiring"}}}
                   }

    )
    def post(self, request):
        if Monthly.objects.filter(is_active=True).exists():
            return Response({"message": "Hozir aktiv oylik mavjud avval aktivlikni o'chiring"}, status=status.HTTP_400_BAD_REQUEST)
        current_month_number = datetime.now().month
        current_year = datetime.now().year
        month_name = MONTHS[current_month_number-1]
        obj = Monthly.objects.create(month=month_name, year=current_year)
        serializer = MonthlySerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StorageViewSet(viewsets.ModelViewSet):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()


class SellCreateAPIView(CreateAPIView):
    serializer_class = SellSerializer
    queryset = Sell.objects.all()

    @extend_schema(
        summary="Yetkazib berish hujjati",
        description="Yetkazob berilgan mahsulotlar",
        tags=["Sell"],
        request=SellCreateSerializer,
        responses={
            status.HTTP_201_CREATED: SellSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = SellCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sell = serializer.save()
        serializer_response = SellSerializer(sell)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)


class ExpenseCreateAPIView(CreateAPIView):
    model = Expense
    serializer_class = ExpenseSerializer

    @extend_schema(
        summary="Xarajatlar hujjati",
        description="Xarajatlar hujjati",
        tags=["Expense"],
        request=ExpenseCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ExpenseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = ExpenseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expense = serializer.save()
        serializer_response = ExpenseSerializer(expense)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)
