from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APIClient

from bank_admin.models import Admin
from client.models import Client as My_Client
from bank.models import Bank


class BankAdminTests(TestCase):

    def setUp(self):
        self.client_1 = APIClient()
        self.client_2 = APIClient()
        self.client_3 = Client(enforce_csrf_checks=False)

        bank = Bank.objects.create(id=3, name='BelBank', country=1, balance=10000, negative_percent=0.1)

        user_1 = User.objects.create(is_staff=True, password=make_password('user_1'), username='user_1')
        user_2 = User.objects.create(is_staff=True, password=make_password('user_2'), username='user_2')

        My_Client.objects.create(id=2, user=user_1, balance=200, bank_fk=bank, country=1)
        My_Client.objects.create(id=3, user=user_2, balance=200, bank_fk=bank, country=1)

        auth_admin = User.objects.create(is_staff=True, is_superuser=True, password=make_password('admin'),
                                         username='admin')
        Admin.objects.create(admin=auth_admin, country=1, bank_fk=bank)

        self.client_1.force_authenticate(auth_admin)
        self.client_3.force_login(user_1)

    def test_operation_list(self):
        auth_request = self.client_1.get(reverse('all_operations'), format='json')
        undefined_request = self.client_2.get(reverse('all_operations'), format='json')

        self.assertEqual(auth_request.status_code, status.HTTP_200_OK)
        self.assertEqual(undefined_request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_operation(self):
        correct_request = self.client_3.post(reverse('create_operation'), {
            "name": "Перевод денег",
            "total": "100",
            "client_fk": 2,
            "destination_fk": 3,
            "bank_fk": 3,
        }, format='json')
        incorrect_request_1 = self.client_1.post(reverse('create_operation'), {}, format='json')
        incorrect_request_2 = self.client_2.post(reverse('create_operation'), {}, format='json')

        self.assertEqual(correct_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(incorrect_request_1.status_code, status.HTTP_403_FORBIDDEN, msg="Forbidden for admin")
        self.assertEqual(incorrect_request_2.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="Forbidden for unauthorized users")

    def test_detail_client_delete(self):
        auth_delete_request = self.client_1.delete(reverse('delete_account'), format='json')

        self.assertEqual(auth_delete_request.status_code, status.HTTP_204_NO_CONTENT)
