from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import *

admin.site.register((Garden,Product,Sell,SellItem,Order,OrderItem,Monthly,MonthlyItem,Expense,ExpenseItem,Storage))
admin.site.unregister((User,Group))