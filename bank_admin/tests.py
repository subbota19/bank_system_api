from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APIClient

import bank_admin.models
from bank.models import Bank


# Create your tests here.


class BankAdminTests(TestCase):

    def setUp(self):
        self.client_1 = APIClient()
        self.client_2 = APIClient()
        self.client_3 = Client(enforce_csrf_checks=False)

        auth_admin = User.objects.create(is_staff=True, is_superuser=True, password=make_password('admin'),
                                         username='admin')
        bank = Bank.objects.create(name='BelBank', country=1, balance=10000)
        bank_admin.models.Admin.objects.create(admin=auth_admin, country=1, bank_fk=bank)

    def test_account_admin(self):
        admin = User.objects.all().get(username='admin')
        self.client_1.force_authenticate(user=admin)

        auth_request = self.client_1.get(reverse('account'), format='json')
        undefined_request = self.client_2.get(reverse('account'), format='json')

        self.assertEqual(auth_request.status_code, status.HTTP_200_OK)
        self.assertEqual(undefined_request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_admin(self):
        correct_request = self.client_3.post(reverse('create_account'), {
            "user.username": "new_admin",
            "user.password": "new_admin",
            "user.email": "new_admin@mail.ru",

            "country": "ru",
            "bank_fk": 1

        }, format='json')
        incorrect_request = self.client_3.post(reverse('create_account'), {}, format='json')

        self.assertEqual(correct_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(incorrect_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_client_delete(self):
        admin = User.objects.all().get(username='admin')
        self.client_1.force_authenticate(user=admin)

        auth_delete_request = self.client_1.delete(reverse('delete_account'), format='json')

        self.assertEqual(auth_delete_request.status_code, status.HTTP_204_NO_CONTENT)
