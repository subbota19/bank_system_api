from rest_framework import serializers
from .models import Client, Bank, User
from bank.serializers import BankSerializer
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class CreateClientSerializer(serializers.ModelSerializer):
    bank_fk = BankSerializer
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['user', 'balance', 'country', 'bank_fk']

    def create(self, validated_data):
        user = dict(validated_data.pop('user'))
        user = User.objects.create(is_staff=True, password=make_password(user.pop('password')), **user)
        return Client.objects.create(user=user, **validated_data)


class DetailClientSerializer(serializers.ModelSerializer):
    bank_fk = BankSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['user', 'balance', 'country', 'bank_fk']
