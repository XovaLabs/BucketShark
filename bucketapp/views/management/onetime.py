import decimal
from ..subroutines.p_subroutine import Subroutines

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import OneTimePaymentForm
from ...models import OneTimePayment, Category
from django.http import HttpResponseForbidden


# A view class that handles one-time payments, ensuring the user is logged in
class OneTimePaymentView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/payment_view.html'  # Template to render
        self.subroutines = Subroutines()  # Initialize subroutines

        # Function mapping for different actions
        self.function_mapping = {
            "save": self.save_payment,  # Save payment information
            "add_new": self.add_new_payment,  # Add a new payment
            "delete": self.delete_payment,  # Delete a payment
        }

    def save_payment(self, request):
        """
        Subroutine to save the information from the form to the database.
        Retrieves the record from the database and updates it with form data.
        """
        print("saved")
        record = OneTimePayment.objects.get(pk=request.POST['id'])  # Get the payment record by ID
        record.source = request.POST['name']  # Update source name
        record.spent = request.POST['spent']  # Update amount spent

        # Get the category from the database
        category = Category.objects.filter(category_name=request.POST['category'])[0]
        print("category: ", category)
        record.category = category  # Update category

        record.description = request.POST['description']  # Update description
        record.date_received = request.POST['date']  # Update date received
        record.save()  # Save changes to the database

    def add_new_payment(self, request):
        """
        Subroutine to add a new one-time payment for the user.
        """
        category_default = Category.objects.filter(category_privacy=False)  # Get default categories
        new_category = OneTimePayment(user=request.user, category=category_default[0])  # Create new payment record
        new_category.save()  # Save new payment to the database

    def delete_payment(self, request):
        """
        Subroutine to delete a one-time payment based on form data.
        """
        print("deleted")
        record = OneTimePayment.objects.get(pk=request.POST['id'])  # Get the payment record by ID
        record.delete()  # Delete the record

    def get(self, request):
        """
        Handle GET requests to display the payment view.
        Filters payments and categories by the logged-in user and renders the template.
        """
        onetime_payments = OneTimePayment.objects.filter(user=request.user)  # Get user's one-time payments
        categories = Category.objects.filter(category_user=request.user)  # Get user's categories

        return render(request, self.template_name, {
            'payment_form': OneTimePaymentForm(),  # Payment form instance
            'payment_records': onetime_payments,  # Payment records
            'payment_name': 'onetime_payment',  # Payment name
            'categories': categories,  # Category records
        })

    def post(self, request):
        """
        Handle POST requests to perform actions based on the form submission.
        Calls the appropriate function based on the 'submit' value in the form.
        """
        self.function_mapping[request.POST['submit']](request)  # Call the appropriate function
        print(request.POST)  # Print the form data for debugging

        return redirect('add_onetime_payment')  # Redirect to the add payment view
