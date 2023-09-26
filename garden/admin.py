from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import *
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class GardenModelAdminForm(forms.ModelForm):
    phone_number = PhoneNumberField(region="UZ")

    class Meta:
        model = Garden
        fields = '__all__'

admin.site.register((Sell,SellItem,OrderItem,Monthly,Limit,LimitItem,Expense,ExpenseItem,Storage))
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

class ProductAdmin(admin.ModelAdmin):
    indexCnt = 0
    list_display = ("index_counter","name","measure")

    def index_counter(self, obj):
        count = Product.objects.all().count()
        if self.indexCnt < count:
            self.indexCnt += 1
        else:
            self.indexCnt = 1
        return  self.indexCnt

    index_counter.short_description = '#'
admin.site.register(Product, ProductAdmin)

class GardenAdmin(admin.ModelAdmin):
    form=GardenModelAdminForm
    indexCnt = 0
    list_display = ("index_counter","name","person","phone_number")
    search_fields = ("person","phone_number")
    ordering = ["name",]

    def index_counter(self, obj):
        count = Garden.objects.all().count()
        if self.indexCnt < count:
            self.indexCnt += 1
        else:
            self.indexCnt = 1
        return  self.indexCnt

    index_counter.short_description = 'TR'
admin.site.register(Garden, GardenAdmin)
# admin.site.title="Mahsulot"