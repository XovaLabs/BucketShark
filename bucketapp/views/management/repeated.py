from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import RepeatedPaymentForm
from ...models import RepeatedPayment, Category
from django.http import HttpResponseForbidden


# A view class that handles repeated payments, ensuring the user is logged in
class RepeatedPaymentView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/payment_view.html'  # Template to render

        # Function mapping for different actions
        self.function_mapping = {
            "save": self.save_payment,  # Save payment information
            "add_new": self.add_new_category,  # Add a new category
            "delete": self.delete_category,  # Delete a category
        }

    def save_payment(self, request):
        """
        Subroutine to save the information from the form to the database.
        Retrieves the record from the database and updates it with form data.
        """
        print("saved")
        record = RepeatedPayment.objects.get(pk=request.POST['id'])  # Get the payment record by ID
        record.source = request.POST['name']  # Update source name
        record.spent = request.POST['spent']  # Update amount spent

        # Get the category from the database
        category = Category.objects.filter(category_name=request.POST['category'])[0]
        print("category: ", category)
        record.category = category  # Update category
        print(request.POST['frequency'])
        record.frequency = request.POST['frequency']  # Update frequency

        record.description = request.POST['description']  # Update description
        record.date_received = request.POST['date']  # Update date received
        record.save()  # Save changes to the database

    def add_new_category(self, request):
        """
        Subroutine to add a new category for the user.
        """
        category_default = Category.objects.filter(category_privacy=False)  # Get default categories
        new_category = RepeatedPayment(user=request.user, category=category_default[0])  # Create new category record
        new_category.save()  # Save new category to the database

    def delete_category(self, request):
        """
        Subroutine to delete a category based on form data.
        """
        print("deleted")
        record = RepeatedPayment.objects.get(pk=request.POST['id'])  # Get the payment record by ID
        record.delete()  # Delete the record

    def get(self, request):
        """
        Handle GET requests to display the payment view.
        Filters payments and categories by the logged-in user and renders the template.
        """
        repeated_payments = RepeatedPayment.objects.filter(user=request.user)  # Get user's repeated payments
        categories = Category.objects.filter(category_user=request.user)  # Get user's categories
        frequencies = ["D", "W", "M", "Y"]  # Possible frequencies
        return render(request, self.template_name, {
            'payment_form': RepeatedPaymentForm(),  # Payment form instance
            'payment_records': repeated_payments,  # Payment records
            'payment_name': 'repeated_payment',  # Payment name
            'categories': categories,  # Category records
            'frequencies': frequencies,  # Frequency options
        })

    def post(self, request):
        """
        Handle POST requests to perform actions based on the form submission.
        Calls the appropriate function based on the 'submit' value in the form.
        """
        self.function_mapping[request.POST['submit']](request)  # Call the appropriate function
        return redirect('add_repeated_payment')  # Redirect to the add payment view
