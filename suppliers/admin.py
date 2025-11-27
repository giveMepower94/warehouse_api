from django.contrib import admin
from .models import Suppliers


# Register your models here.
@admin.register(Suppliers)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("organization_name",
                    "country", "city",
                    "street",
                    "building")
    search_fields = ("organization_name", "country", "city")
    list_filter = ("country",)
