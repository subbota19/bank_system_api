from django.contrib import admin
from .models import Client


class AdminClient(admin.ModelAdmin):
    list_display = ['name', 'email', 'country', 'balance', 'bank']

    @staticmethod
    def name(obj):
        return obj.user.username

    @staticmethod
    def password(obj):
        return obj.user.password

    @staticmethod
    def email(obj):
        return obj.user.email

    @staticmethod
    def bank(obj):
        return obj.bank_fk.name


admin.site.register(Client, AdminClient)
