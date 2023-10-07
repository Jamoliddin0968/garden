# myapp/forms.py
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import *


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()


admin.site.register(
                     Storage)
admin.site.unregister((User, Group))


class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 1


class LimitItemInline(admin.TabularInline):
    model = LimitItem
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class SellItemInline(admin.TabularInline):
    model = SellItem
    extra = 1


@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    inlines = (SellItemInline,)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    indexCnt = 0
    list_display = ("index_counter", "name", "measure")

    def index_counter(self, obj):
        count = Product.objects.all().count()
        if self.indexCnt < count:
            self.indexCnt += 1
        else:
            self.indexCnt = 1
        return self.indexCnt

    index_counter.short_description = '#'


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    indexCnt = 0
    list_display = ("index_counter", "name", "person", "phone_number")
    search_fields = ("person", "phone_number")
    ordering = ["name",]

    def index_counter(self, obj):
        count = Garden.objects.all().count()
        if self.indexCnt < count:
            self.indexCnt += 1
        else:
            self.indexCnt = 1
        return self.indexCnt

    index_counter.short_description = 'TR'


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    inlines = (LimitItemInline,)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    inlines = (ExpenseItemInline,)

# ADMIN_SITE_HEADER = ''


@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    pass
