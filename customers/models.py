from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.last_name} - {self.first_name}"
