import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet.settings')
django.setup()

import requests
import json
from store.models import ProductCard, Pictures
from pet.hidden_data import auth_data

from celery import shared_task, app


@shared_task
def data_input():
    response = {}
    auth_url = "https://office.hubber.pro/api/v1/auth"
    url_response = requests.get(url=auth_url, auth=auth_data).json()
    token = url_response['token']
    # print(url_response)
    #print(token)
    headers = {
        'Authorization': f"Bearer {token}",
        "accept-language": "uk-UA",
    }
    product_url = "http://office.hubber.pro/ru/api/v1/product"
    product_response = requests.get(url=product_url, headers=headers)
    r_status = product_response.status_code
    # products_response = product_response.json()
    # print(products_response)
    count = 0
    page_number = 55
    # while r_status == 200:
    if r_status == 200:

        product_url = f"http://office.hubber.pro/ru/api/v1/product/index?page={page_number}&limit=100"
        page_number += 1
        product_response = requests.get(url=product_url, headers=headers)
        r_status = product_response.status_code
        products_response = product_response.json()
        upload_data_str = json.dumps(products_response)
        upload_data = json.loads(upload_data_str)
        for data in upload_data:
            if data.get("name") != None:
                product = ProductCard(
                    id=data.get("id"),
                    name=data.get("name"),
                    category=data.get("category_name"),
                    vendor_code=data.get("vendor_code"),
                    price=data.get("price"),
                    old_price=data.get("old_price"),
                    availability=data.get("availability"),
                    description=data.get("description"),
                    brand=data.get("brand"),
                    main_picture=data.get("main_picture"),
                    options=data.get("options"),
                    attributes=data.get("attributes"),
                )
                # print(product)
                product.save()
                # print(f"Error in {data.get('name')}")
                # print(data.get("pictures"))
                for input_image in data.get("pictures"):
                    image = Pictures(
                        pictures_point=product,
                        pictures=input_image,
                    )
                    image.save()
                    # print("Image =", image)
                # print(category)
                # print(product)
                count += 1
                print(count)
            else:
                print(data.get("name"))

        response['status'] = 201
        response['message'] = 'success'
        response['count'] = count
    else:
        response['status'] = product_response.status_code
        response['message'] = 'error'
        response['count'] = count

    print(response)


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