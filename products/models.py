from django.db import models
from suppliers.models import Suppliers
from categories.models import Category


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
