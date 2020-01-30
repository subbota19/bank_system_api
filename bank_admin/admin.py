from django.contrib import admin
from .models import Admin


class MainAdmin(admin.ModelAdmin):
    list_display = ['get_user_fk', 'get_bank_fk', 'country']

    @staticmethod
    def get_user_fk(obj):
        return obj.admin.username

    @staticmethod
    def get_bank_fk(obj):
        return obj.bank_fk.name


admin.site.register(Admin, MainAdmin)
