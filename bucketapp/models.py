from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=15)
    category_privacy = models.BooleanField()

    def __str__(self):
        return self.category_name


class BasePayment(models.Model):
    budget_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)  # source or name
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date_received = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True  # This makes BasePayment an abstract base class


class RepeatedPayment(BasePayment):
    FREQUENCY_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES)
    next_payment_date = models.DateField()


class OneTimePayment(BasePayment):
    pass  # No additional fields needed for one-time payments
