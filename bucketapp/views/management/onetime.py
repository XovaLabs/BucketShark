import decimal

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import OneTimePaymentForm
from ...models import OneTimePayment, Category
from django.http import HttpResponseForbidden


class OneTimePaymentView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/payment_view.html'

        #  function mapping
        self.function_mapping = {
            "save": self.save_payment,
            "add_new": self.add_new_payment,
            "delete": self.delete_payment,
        }

        self.category_update_actions = {
            "save": self.update_spent_category_saving,
            "add_new": self.update_spent_category_add,
            "delete": self.update_spent_category_delete,
        }

    def save_payment(self, request):
        print("saved")
        self.category_update_actions[request.POST['submit']](request)

        record = OneTimePayment.objects.get(pk=request.POST['id'])
        record.source = request.POST['name']
        record.spent = request.POST['spent']
        record.description = request.POST['description']
        record.date_received = request.POST['date']
        record.save()

    def add_new_payment(self, request):
        category_default = Category.objects.filter(category_privacy=False)
        new_category = OneTimePayment(user=request.user, category=category_default[0])
        new_category.save()

    def delete_payment(self, request):
        print("deleted")
        record = OneTimePayment.objects.get(pk=request.POST['id'])
        record.delete()

    def update_spent_category_saving(self, request):
        category = Category.objects.get(pk=request.POST['id'])
        o_payment = OneTimePayment.objects.get(pk=request.POST['id'])
        print(o_payment)
        category.spent = category.spent - o_payment.spent
        print(category.spent)
        print(request.POST['spent'])
        category.spent = category.spent + decimal.Decimal(request.POST['spent'])
        category.save()

    def update_spent_category_add(self, request):
        category = Category.objects.get(pk=request.POST['id'])
        category.spent += request.POST['spent']
        category.save()

    def update_spent_category_delete(self, request):
        category = Category.objects.get(pk=request.POST['id'])
        category.spent -= int(request.POST['spent'])
        category.save()

    def get(self, request):
        # Filter payments by the logged-in user
        onetime_payments = OneTimePayment.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'payment_form': OneTimePaymentForm(),
            'payment_records': onetime_payments,
            'payment_name': 'onetime_payment',
        })

    def post(self, request):
        self.function_mapping[request.POST['submit']](request)

        return redirect('add_onetime_payment')
