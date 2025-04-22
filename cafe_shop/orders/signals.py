from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Order

@receiver(post_delete, sender=Order)
def update_something_on_order_delete(sender, instance, **kwargs):
    """
    Пример сигнала: выполняется после удаления заказа.
    Например, можно обновить статистику или отправить уведомление.
    """
    print(f"Заказ {instance.id} удалён!")