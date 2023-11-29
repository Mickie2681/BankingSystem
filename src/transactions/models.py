from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = settings.AUTH_USER_MODEL


class Diposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(max_length=10)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
