from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APIClient

import client.models
from bank.models import Bank


class ClientTests(TestCase):

    def setUp(self):
        self.client_1 = APIClient()
        self.client_2 = APIClient()
        self.client_3 = Client(enforce_csrf_checks=False)

        auth_user = User.objects.create(is_staff=True, password=make_password('user'), username='user')
        bank = Bank.objects.create(name='BelBank', country=1, balance=10000)
        client.models.Client.objects.create(user=auth_user, country=1, bank_fk=bank, balance=100)

    def test_account_client(self):
        user = User.objects.all().get(username='user')
        self.client_1.force_authenticate(user=user)
        auth_request = self.client_1.get(reverse('account'), format='json')
        undefined_request = self.client_2.get(reverse('account'), format='json')

        self.assertEqual(auth_request.status_code, status.HTTP_200_OK)
        self.assertEqual(undefined_request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_client(self):
        correct_request = self.client_3.post(reverse('create_account'), {
            "user.username": "new_user",
            "user.password": "new_user",
            "user.email": "new_user@mail.ru",

            "balance": "100",
            "country": "ru",
            "bank_fk": 1

        }, format='json')
        incorrect_request = self.client_3.post(reverse('create_account'), {}, format='json')

        self.assertEqual(correct_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(incorrect_request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_client_get(self):
        user = User.objects.all().get(username='user')
        self.client_1.force_authenticate(user=user)

        auth_get_request = self.client_1.get(reverse('edit_account'), format='json')
        undefined_get_request = self.client_2.get(reverse('edit_account'), format='json')

        self.assertEqual(auth_get_request.status_code, status.HTTP_200_OK)
        self.assertEqual(undefined_get_request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_client_delete(self):
        user = User.objects.all().get(username='user')
        self.client_1.force_authenticate(user=user)

        auth_delete_request = self.client_1.delete(reverse('edit_account'), format='json')

        self.assertEqual(auth_delete_request.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_client_put(self):
        user = User.objects.all().get(username='user')
        self.client_1.force_authenticate(user=user)

        auth_put_request = self.client_1.put(reverse('edit_account'), {'balance': 1000, 'country': 'ru'}, format='json')

        self.assertEqual(auth_put_request.status_code, status.HTTP_200_OK)
        self.assertEqual(float(auth_put_request.data['balance']), 1000)
