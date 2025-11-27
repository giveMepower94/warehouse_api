from django.contrib import admin
from .models import Customers


# Register your models here.
@admin.register(Customers)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "last_name", "first_name", "age")
    search_fields = ("last_name", "first_name", "user__username")
    list_filter = ("age",)
