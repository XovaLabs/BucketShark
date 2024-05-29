from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import Category, RepeatedPayment, OneTimePayment


class Dashboard(LoginRequiredMixin, TemplateView):
    def __init__(self):
        super().__init__()
        self.template_name = 'bucketapp/dashboard.html'
        self.sum_mapping = {"category": self.category_spent_sum, "payment": self.payment_dict_sum}

    def category_spent_sum(self):
        pass  # TODO: Implement the category_spent_sum method

    def payment_dict_sum(self, payment_list_dict):
        payment_sum = 0
        for payment in payment_list_dict:
            #print(f'''{payment["payment"]["name"]}: ''', payment["payment"]["spent"])
            payment_sum += payment["payment"]["spent"]
        print(f"payment sum: {payment_sum}")
        return payment_sum

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        print(user)  # TODO: Remove or handle debug prints appropriately
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
                payment_struct = {
                    "payment": {
                        "name": payment.source,
                        "spent": payment.spent,
                        "date": payment.date_received
                    }}

                if payment.category == category:
                    onetime_p.append(payment_struct)

                if payment.category.category_name == "Income":
                    income_p.append(payment.spent)
                else:
                    expense_p.append(payment.spent)

            for payment in repeated_payments:
                payment_struct = {
                        "payment": {
                            "name": payment.source,
                            "spent": payment.spent,
                            "date": payment.date_received,
                            "frequency": payment.frequency
                        }}
                if payment.category == category:
                    rep_p.append(payment_struct)

                if payment.category.category_name == "Income":
                    income_p.append(payment.spent)
                else:
                    expense_p.append(payment.spent)

            print(f"repeated payment: {rep_p}")  # TODO: Remove or handle debug prints appropriately
            print()
            print(f"one time payments: {onetime_p}")  # TODO: Remove or handle debug prints appropriately
            rep_payment_sum = self.sum_mapping["payment"](rep_p)
            onetime_payment_sum = self.sum_mapping["payment"](onetime_p)
            category_spent[category.category_name] = rep_payment_sum + onetime_payment_sum
            onetime_p = []
            rep_p = []

        print("Category Spent: ", category_spent, "< End of CATEGORY SPENT")  # TODO: Remove or handle debug prints

        # Calculate account balance
        total_income = sum(income_p)
        print(total_income)  # TODO: Remove or handle debug prints appropriately

        total_expenses = sum(expense_p)
        print(total_expenses)  # TODO: Remove or handle debug prints appropriately

        account_balance = total_income - total_expenses
        print(account_balance)  # TODO: Remove or handle debug prints appropriately

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
