from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    negative_percent = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    country = models.CharField(max_length=2,
                               choices=[('ru', 'russia'), ('by', 'belarus'), ('ua', 'ukraine'), ('pl', 'poland')])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
