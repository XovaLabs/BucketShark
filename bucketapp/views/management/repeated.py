from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import RepeatedPaymentForm
from ...models import RepeatedPayment, Category
from django.http import HttpResponseForbidden


class RepeatedPaymentView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/payment_view.html'

        #  function mapping
        self.function_mapping = {"save": self.save_payment,
                                 "add_new": self.add_new_category,
                                 "delete": self.delete_category,
                                 }

    def save_payment(self, request):
        """
        Sub routine to save the information from the form to the database. record is an instance of the database and
        updates the information directly from the form information.
        """
        print("saved")
        record = RepeatedPayment.objects.get(pk=request.POST['id'])
        record.source = request.POST['name']
        record.spent = request.POST['spent']
        #  TODO: update category frequency
        category = Category.objects.filter(category_name=request.POST['category'])[0]
        print("category: ", category)
        record.category = category

        record.description = request.POST['description']
        record.date_received = request.POST['date']
        record.save()

    def add_new_category(self, request):
        category_default = Category.objects.filter(category_privacy=False)
        new_category = RepeatedPayment(user=request.user, category=category_default[0])
        new_category.save()

    def delete_category(self, request):
        print("deleted")
        record = RepeatedPayment.objects.get(pk=request.POST['id'])
        record.delete()

    def get(self, request):
        # Filter payments by the logged-in user
        repeated_payments = RepeatedPayment.objects.filter(user=request.user)
        categories = Category.objects.filter(category_user=request.user)
        frequencies = ["D", "W", "M", "Y", ]
        return render(request, self.template_name, {
            'payment_form': RepeatedPaymentForm(),
            'payment_records': repeated_payments,
            'payment_name': 'repeated_payment',
            'categories': categories,
            'frequencies': frequencies,
        })

    def post(self, request):

        self.function_mapping[request.POST['submit']](request)
        return redirect('add_repeated_payment')
