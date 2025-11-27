from django.db import models


# Create your models here.
class Suppliers(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=20)
    organization_name = models.CharField(max_length=255)

    def __str__(self):
        return self.organization_name
