from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import Category, RepeatedPayment, OneTimePayment


class Dashboard(LoginRequiredMixin, TemplateView):
    def __init__(self):
        super().__init__()
        self.template_name = 'bucketapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        print(user)
        categories = Category.objects.filter(category_user=user)
        one_time_payments = OneTimePayment.objects.filter(user=user)
        repeated_payments = RepeatedPayment.objects.filter(user=user)

        income_p = []
        expense_p = []

        onetime_p = []
        rep_p = []

        # Calculate total spent for each category
        category_spent = {}
        for category in categories:
            for payment in one_time_payments:
                print(payment.category)
                if payment.category == category:
                    onetime_p.append(payment.spent)

                if payment.category.category_name == "Income":
                    income_p.append(payment.spent)
                else:
                    expense_p.append(payment.spent)

            for payment in repeated_payments:
                if payment.category == category:
                    rep_p.append(payment.spent)

                if payment.category.category_name == "Income":
                    income_p.append(payment.spent)
                else:
                    expense_p.append(payment.spent)

            category_spent[category] = sum(onetime_p) + sum(rep_p)

        print(category_spent)
        # Calculate account balance
        total_income = sum(income_p)
        print(income_p)
        print(total_income)

        total_expenses = sum(expense_p)
        print(total_expenses)
        account_balance = total_income - total_expenses
        print(account_balance)

        # Estimate account balance over time
        time_period = 12  # Number of months to estimate
        estimated_account_balance = [account_balance]
        for i in range(1, time_period):
            account_balance -= total_expenses / time_period
            estimated_account_balance.append(account_balance)

        context['categories'] = categories
        context['category_spent'] = category_spent
        context['estimated_account_balance'] = estimated_account_balance

        return context

