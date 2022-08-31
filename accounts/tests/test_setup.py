from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('registration')

        self.user_data = {
            "password": "123456789resY!",
            "password2": "123456789resY!",
            "email": "testuser@mail.ru"
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
