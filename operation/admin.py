from django.contrib import admin
from .models import Operation


class AdminOperation(admin.ModelAdmin):
    list_display = ['name', 'total', 'is_valid', 'client_fk', 'destination_fk']

    @staticmethod
    def client_fk(obj):
        return obj.client_fk.username

    @staticmethod
    def destination_fk(obj):
        return obj.destination_fk.name


admin.site.register(Operation, AdminOperation)
