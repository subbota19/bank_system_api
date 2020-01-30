from django.db import models
from client.models import Client
from bank.models import Bank


class Operation(models.Model):
    name = models.CharField(max_length=30)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    is_valid = models.BooleanField(default=False)

    client_fk = models.ForeignKey(Client, related_name='client_fk', on_delete=models.CASCADE)
    destination_fk = models.ForeignKey(Client, related_name='destination_fk', on_delete=models.CASCADE)
    bank_fk = models.ForeignKey(Bank, related_name='bank_fk', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Operation'
        verbose_name_plural = 'Operations'

    def delete(self, *args, **kwargs):
        bank_percent = self.total * self.bank_fk.negative_percent
        self.client_fk.balance += self.total
        self.destination_fk.balance -= (self.total + bank_percent)
        self.bank_fk.balance -= bank_percent
        super(Bank, self.bank_fk).save(*args, **kwargs)
        super(Client, self.client_fk).save(*args, **kwargs)
        super(Client, self.destination_fk).save(*args, **kwargs)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.client_fk.balance >= self.total:
            self.is_valid = True
        if self.is_valid:
            bank_percent = self.total * self.bank_fk.negative_percent
            self.client_fk.balance -= self.total
            self.bank_fk.balance += bank_percent
            self.destination_fk.balance += (self.total - bank_percent)
            super(Bank, self.bank_fk).save(*args, **kwargs)
            super(Client, self.client_fk).save(*args, **kwargs)
            super(Client, self.destination_fk).save(*args, **kwargs)
        super().save(self, *args, **kwargs)
