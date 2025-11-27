from django.contrib import admin
from .models import Product, Stock


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    passlist_display = ("name", "supplier", "category", "price")
    list_filter = ("supplier", "category")
    search_fields = ("name",)
    inlines = [StockInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")
    search_fields = ("product__name",)
