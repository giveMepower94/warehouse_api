from .serializers import SupplierSerializer
from .models import Suppliers
from rest_framework import viewsets


# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SupplierSerializer
