from django.db import models
from bank.models import Bank
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=2,
                               choices=[('ru', 'russia'), ('by', 'belarus'), ('ua', 'ukraine'), ('pl', 'poland')])
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    bank_fk = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
