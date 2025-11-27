from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer__last_name", "customer__first_name")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    passlist_display = ("order", "product", "quantity", "purchase_price")
    search_fields = ("product__name",)
