from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import RepeatedPaymentForm, OneTimePaymentForm
from ...models import RepeatedPayment, OneTimePayment
from django.http import HttpResponseForbidden


class OneTimePaymentView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/payment_view.html'

    def get(self, request):
        # Filter payments by the logged-in user
        repeated_payments = RepeatedPayment.objects.filter(user=request.user)
        onetime_payments = OneTimePayment.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'payment_form': OneTimePaymentForm(),
            'payment_records': onetime_payments,
            'payment_name': 'onetime_payment',
        })

    @staticmethod
    def post(request):
        if 'onetime_payment' in request.POST:
            form = OneTimePaymentForm(request.POST)
            if form.is_valid():
                onetime_payment = form.save(commit=False)
                onetime_payment.user = request.user
                onetime_payment.save()
            # Implement logic for edit and delete
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

        return redirect('add_onetime_payment')
