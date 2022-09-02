from rest_framework.test import APITestCase

from accounts.models import CustomUser


class TestCustomUserModel(APITestCase):

    def setUp(self) -> None:
        CustomUser.objects.create(
            email='testuser@mail.ru',
            username='TestUser',
            first_name='Test',
            last_name='User'
        )

    def tearDown(self) -> None:
        pass

    def test_email_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email')

    def test_username_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'Username')
