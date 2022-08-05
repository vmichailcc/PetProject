from django.db.models import signals
from django.dispatch import receiver
from .models import Order


@receiver(signals.pre_save, sender=Order)
def create_product(instance, **kwargs):
    last_status = Order.objects.get(pk=instance.pk)
    if instance.status != last_status.status:
        print("***" * 10, "\n", f"new status = {instance.status}", "\n", "***" * 10)
