import datetime  # Importing the datetime module for handling date-related tasks

from django.db import models  # Importing Django's model module for defining database models
from django.contrib.auth.models import User  # Importing Django's built-in User model for authentication
from django.utils import timezone  # Importing timezone utilities from Django

# Models


class Category(models.Model):
    # Model representing a category for budgeting purposes
    category_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key field
    category_user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key linking to the User model,
    # with cascading delete
    category_name = models.CharField(max_length=15)  # CharField for the category name with a max length of 15
    # characters
    category_privacy = models.BooleanField()  # Boolean field indicating if the category is private
    budgeted = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Decimal field for the budgeted
    # amount
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Decimal field for the amount spent
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Decimal field for the balance

    def __str__(self):
        # String representation of the Category model, returning the category name
        return self.category_name


class BasePayment(models.Model):
    # Abstract base model for payments
    budget_id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key field
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key linking to the User model,
    # with cascading delete
    source = models.CharField(max_length=100, default='empty')  # CharField for the payment source or name,
    # with a default value
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Decimal field for the amount spent
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # Foreign key linking to the Category
    # model, with cascading delete
    date_received = models.DateField(default=timezone.now)  # Date field for the date received, with default set
    # to current date
    description = models.TextField(blank=True)  # Text field for the description, which can be blank

    class Meta:
        abstract = True  # Marks this model as an abstract base class, meaning it won't create a separate table
        # in the database


class RepeatedPayment(BasePayment):
    # Model for repeated payments, inheriting from BasePayment
    FREQUENCY_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]  # Choices for the frequency of payments
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, default='W')  # CharField for the frequency,
    # with choices and a default value
    next_payment_date = models.DateField(default=datetime.date.today())  # Date field for the next payment date, with
    # default set to today's date


class OneTimePayment(BasePayment):
    # Model for one-time payments, inheriting from BasePayment
    pass  # No additional fields needed for one-time payments
