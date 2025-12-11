from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from products.models import Stock
from .models import Order, OrderItem
from .tasks import send_order_email_task


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'purchase_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'items']
        read_only_fields = ['id', 'created_at']

    def validate_items(self, items):
        for i, item in enumerate(items):
            qty = item.get('quantity')
            if qty is None or qty <= 0:
                raise serializers.ValidationError({i: "Quantity must be positive."})
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():
            product_ids = [item['product'].id for item in items_data]
            stocks_qs = Stock.objects.select_for_update().filter(product_id__in=product_ids)
            stocks_by_product = {s.product_id: s for s in stocks_qs}

            # Проверка остатков
            errors = []
            for idx, item in enumerate(items_data):
                pid = item['product'].id
                qty = item['quantity']
                stock = stocks_by_product.get(pid)
                if stock is None:
                    errors.append({idx: f"Product id {pid} has no stock record."})
                elif stock.quantity < qty:
                    errors.append({idx: f"Not enough stock for product id {pid}. Available: {stock.quantity}"})
            if errors:
                raise serializers.ValidationError({'items': errors})

            # Создаем заказ
            order = Order.objects.create(**validated_data)

            # Списываем остатки + создаем позиции заказа
            for item in items_data:
                pid = item['product'].id
                qty = item['quantity']
                stock = stocks_by_product[pid]

                stock.quantity = F('quantity') - qty
                stock.save(update_fields=['quantity'])
                stock.refresh_from_db()

                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=qty,
                    purchase_price=item.get('purchase_price')
                )

        # После успешной транзакции отправляем email
        send_order_email_task.delay(order.id)

        return order
