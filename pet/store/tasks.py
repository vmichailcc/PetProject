import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet.settings')
django.setup()

import requests
import json
from store.models import ProductCard, Pictures
from pet.hidden_data import auth_data
from celery import shared_task


# @shared_task
# def sample_task():
#     print("Ukraine win!")


@shared_task
def data_input():
    response = {}
    auth_url = "https://office.hubber.pro/api/v1/auth"
    url_response = requests.get(url=auth_url, auth=auth_data).json()
    token = url_response['token']
    headers = {
        'Authorization': f"Bearer {token}",
        "accept-language": "uk-UA",
    }
    product_url = "http://office.hubber.pro/ru/api/v1/product/index?page=1&limit=100"
    product_response = requests.get(url=product_url, headers=headers)
    pagination_page_number = int(product_response.headers['x-pagination-page-count'])
    # print("pagination_page_number =", pagination_page_number)
    # r_status = product_response.status_code
    count = 0
    page_number = 1
    while page_number <= pagination_page_number:
        # if r_status == 200:
        try:
            product_url = f"http://office.hubber.pro/ru/api/v1/product/index?page={page_number}&limit=100"
            #print("Page -", page_number, "from", pagination_page_number)
            page_number += 1
            product_response = requests.get(url=product_url, headers=headers)
            r_status = product_response.status_code
            #print("\t Status -", r_status)

            products_response = product_response.json()
            upload_data_str = json.dumps(products_response)
            upload_data = json.loads(upload_data_str)
            # print("upload_data =", upload_data)
            for data in upload_data:
                if data.get("name") is not None:
                    #print(data.get("id"), "\n***")
                    if data.get("name") is not None:
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
                        product.save()
                    for input_image in data.get("pictures"):
                        image = Pictures(
                            pictures_point=product,
                            pictures=input_image,
                        )
                        image.save()

                    count += 1
                else:
                    continue
        except ValueError:
            raise "Data input error!"
        response['status'] = product_response.status_code
        response['message'] = 'error'
        response['count'] = count
    else:
        response['status'] = product_response.status_code
        response['message'] = 'success'
        response['count'] = count
    # from store.store_input_data import data_input as d
    print(response)


@shared_task
def delete_data():
    data = ProductCard.objects.filter(availability=0).delete()
    print(data)
