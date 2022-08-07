from django.db.models import signals
from django.dispatch import receiver
from .models import Order
from accounts.tasks import send_status_email_celery
from django.core.exceptions import ObjectDoesNotExist


@receiver(signals.pre_save, sender=Order)
def create_product(sender, instance, **kwargs):
    if Order.objects.filter(pk=instance.pk):
        last_status = Order.objects.get(pk=instance.pk)
        if instance.status != last_status.status:
            send_status_email_celery.delay(instance.pk, instance.get_status_display())



    # try:
    #     Order.objects.get(pk=instance.pk)
    # except ObjectDoesNotExist:
    #     last_status = Order.objects.get(pk=instance.pk)
    #     if instance.status != last_status.status:
    #         send_status_email_celery.delay(instance.pk, instance.get_status_display())

