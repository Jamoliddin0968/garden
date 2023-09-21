from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import *

admin.site.register((Garden,Product,Sell,SellItem,OrderItem,Monthly,Limit,LimitItem,Expense,ExpenseItem,Storage))
admin.site.unregister((User,Group))

# buyurtm
def view_order_items(modeladmin, request, queryset):
    # print(queryset)
    for order in queryset:
        items = OrderItem.objects.filter(order=order)
        product_list = "\n".join([str(item) for item in items])
        message = f"items in category '{order}':\n{product_list}"
        modeladmin.message_user(request, message)

view_order_items.short_description = "View Products for Selected Category"

class OrderAdmin(admin.ModelAdmin):
    actions = [view_order_items]
admin.site.register(Order, OrderAdmin)