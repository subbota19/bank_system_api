from django.contrib import admin
from .models import Bank


class AdminBank(admin.ModelAdmin):
    list_display = ['name', 'balance', 'country','negative_percent']



admin.site.register(Bank, AdminBank)
