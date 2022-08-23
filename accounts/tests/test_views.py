from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser


class UserRegisterTest(APITestCase):
    def test_create_account(self):
        url = reverse('registration')
        data = {
            "username": "TestUser",
            "password": "12345678910resY",
            "password2": "12345678910resY",
            "email": "ara@mail.ru",
            "first_name": "GreenLand",
            "last_name": "Johnykson"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'TestUser')
