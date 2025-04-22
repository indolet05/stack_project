from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('completed', 'Выполнен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Заказ #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    instance.order.calculate_total()