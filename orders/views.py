from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from .models import Order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Пользователи видят только свои заказы, админ видит все.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        """
        Привязываем заказ к текущему пользователю.
        Отправка письма происходит внутри сериализатора.
        """
        customer = self.request.user.customers
        serializer.save(customer=customer)