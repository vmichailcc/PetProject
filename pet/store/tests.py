from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import ProductCard, Order
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser


'''
Покрити тестами всі API ендпоінти:
-	Позитивний тест;
-	Негативний тест;
-	Тести на валідації та доступів;
-	Тести на фільтри, пошук та ордерінг.
'''


class StoreTests(APITestCase):

    def setUp(self):
        test_user = CustomUser.objects.create(
            first_name="Mike",
            last_name="Test",
            city="Zp",
            email="test@test.com",
        )
        test_user.save()
        self.user_token = Token.objects.create(user=test_user)

        test_product = ProductCard.objects.create(
            id="8888Qwerty",
            name="Тестова картина",
            category="Тестова категорія",
            vendor_code="99As",
            price="999",
            old_price="1111",
            description="Тестовий опис продукту",
            brand="Козак",
            main_picture="https://image.hubber.pro/ea157ef450c833ef7f3265411c97d670.jpg",
        )
        test_product.save()


    def test_store_list_pos(self):
        url = reverse('store_router-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_store_list_neg(self):
        url = reverse('store_router-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_add_comment_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('comment_router-list')
        data = {
            "text_product": "8888Qwerty",
            "text": "test comment 1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('comment_router-list')
        data = {
            "text_product": "error",
            "text": "test comment 1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_order_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_order_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "100"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_owner_order_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_owner_order_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {

        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_product_detail_pos(self):
        url = reverse('product_router-detail', kwargs={"pk": "8888Qwerty"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_product_detail_neg(self):
        url = reverse('product_router-detail', kwargs={"pk": "1"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response = self.client.post(url, data, format('json'))
        url = reverse('order_detail_router-detail', kwargs={"pk": "2"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_order_detail_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        url = reverse('order_detail_router-detail', kwargs={"pk": "404"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)