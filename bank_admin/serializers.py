from rest_framework import serializers
from .models import Admin, User
from client.serializers import UserSerializer
from bank.serializers import BankSerializer
from django.contrib.auth.hashers import make_password


class CreateAdminSerializer(serializers.ModelSerializer):
    bank_fk = BankSerializer
    admin = UserSerializer()

    class Meta:
        model = Admin
        fields = ['admin', 'country', 'bank_fk']

    def create(self, validated_data):
        user = dict(validated_data.pop('admin'))
        user = User.objects.create(is_staff=True, password=make_password(user.pop('password')), **user)
        return Admin.objects.create(admin=user, **validated_data)
