from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import RepeatedPaymentForm
from ...models import RepeatedPayment, OneTimePayment, Category
from django.http import HttpResponseForbidden


class RepeatedPaymentView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/payment_view.html'

    def get(self, request):
        # Filter payments by the logged-in user
        repeated_payments = RepeatedPayment.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'payment_form': RepeatedPaymentForm(),
            'payment_records': repeated_payments,
            'payment_name': 'repeated_payment',
        })

    @staticmethod
    def post(request):
        print(request.POST)
        if 'add_new' in request.POST:
            category_default = Category.objects.filter(category_privacy=False)

            repeated_payment = RepeatedPayment(user=request.user, category=category_default[0])
            repeated_payment.save()
        if 'repeated_payment' in request.POST:
            form = RepeatedPaymentForm(request.POST)
            if form.is_valid():
                repeated_payment = form.save(commit=False)
                repeated_payment.user = request.user
                repeated_payment.save()
        elif 'edit_payment' in request.POST:
            # Add your logic here to edit a payment
            pass
        elif 'delete_payment' in request.POST:
            payment_id = request.POST.get('payment_id')
            payment_type = request.POST.get('payment_type')

            # Check if the payment is owned by the user
            if payment_type == 'repeated':
                payment = RepeatedPayment.objects.filter(id=payment_id, user=request.user).first()
            else:
                payment = OneTimePayment.objects.filter(id=payment_id, user=request.user).first()

            if payment:
                payment.delete()
            else:
                return HttpResponseForbidden("You do not have permission to delete this payment.")

        return redirect('add_repeated_payment')
