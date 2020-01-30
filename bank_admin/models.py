from django.db import models
from django.contrib.auth.models import User
from bank.models import Bank


class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=2,
                               choices=[('ru', 'russia'), ('by', 'belarus'), ('ua', 'ukraine'), ('pl', 'poland')])

    bank_fk = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.username

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def save(self, *args, **kwargs):
        self.admin.is_staff = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.admin.delete()
        super().delete(*args, **kwargs)
