from django.db import models


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               related_name='subcategories')
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
