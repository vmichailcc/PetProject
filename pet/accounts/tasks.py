from django.contrib.auth import get_user_model

from celery import shared_task, app
from django.core.mail import EmailMessage


@shared_task
def send_status_email():
    email = EmailMessage(
        "Selery task worker",
        "this is proof",
        to=["var-m@meta.ua"]
    )
    email.send()

# from store.models import Order

# def email_celery():
#     c = Order.objects.get(pk=3)
#     if c.stusus is choise:
#     print(data)



# @app.task
# def send_post_creation_email(subscriber_id, subject, message):
#     UserModel = get_user_model()
#
#     try:
#         subscriber = UserModel.objects.get(pk=subscriber_id)
#     except UserModel.DoesNotExist:
#         logging.warning(f'Tried to send verification email to '
#                         f'non-existing user `{subscriber}`')
#     send_mail(
#         subject,
#         message,
#         'from@quickpublisher.dev',
#         [subscriber.email],
#         fail_silently=False,)