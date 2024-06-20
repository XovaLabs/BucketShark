import decimal

from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import Category, RepeatedPayment, OneTimePayment

import random


class Dashboard(LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()
        self.template_name = 'bucketapp/dashboard.html'
        self.sum_mapping = {"category": self.category_spent_sum, "payment": self.payment_dict_sum}

        self.category_frequency_map = {"W": self.sub_weekly, "M": self.sub_monthly, "Y": self.sub_yearly}

    def graph_strap(self, request):
        payment_dataset = []

        user = self.request.user
        categories = Category.objects.filter(category_user=user)
        one_time_payments = OneTimePayment.objects.filter(user=user)
        repeated_payments = RepeatedPayment.objects.filter(user=user)

        total_income = 0
        total_expense = 0

        for category in categories:
            payments = repeated_payments.filter(category=category)
            category_spent = 0
            for payment in payments:
                category_spent += payment.spent
            category.spent = category_spent
            category.save()
            print("Category spent in",category.category_name, category.spent)
            name = f"{category.category_name}"
            list_of_vals = []
            list_of_vals = self.category_frequency_map['M'](list_of_vals, category)
            payment_dataset.append({"label": name, "data": list_of_vals})


            if category.category_name.lower() == 'income':
                print("New Entry: ", category.category_name.lower())
                total_income += category_spent
            else:
                total_expense += category_spent

        # Calculate account balance
        account_balance = total_income - total_expense
        balance_list_of_vals = [float(account_balance) - sum(
            payment['data'][i] for payment in payment_dataset if payment['label'].lower() != 'income') for i in
                                range(12)]
        payment_dataset.append({"label": "Account Balance", "data": balance_list_of_vals})

        print(payment_dataset)
        return payment_dataset

    def sub_weekly(self, list_of_vals, category):
        category_spent = float(category.spent)

        for x in range(1, 53):  # Change to 53 to include 52 items
            list_of_vals.append(category_spent)
            category_spent += float(category.spent)

        grouped_sums = []

        for i in range(0, len(list_of_vals), 4):
            grouped_sum = sum(float(list_of_vals[i:i + 4]))
            grouped_sums.append(grouped_sum)

        return grouped_sums

    def sub_monthly(self, list_of_vals, category):
        category_spent = float(category.spent)
        for x in range(1, 13):
            list_of_vals.append(category_spent)
            category_spent += float(category.spent)
        return list_of_vals

    def sub_yearly(self, list_of_vals, category):
        category_spent = float(category.spent)
        for x in range(1, 11):
            list_of_vals.append(category_spent)
            if x != 10:
                category_spent += float(category.spent)
            else:
                category_spent += float(category.spent)
        return list_of_vals

    def generate_random_colors(self, num_colors):
        colors = set()
        while len(colors) < num_colors:
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            colors.add(color)
        return list(colors)

    def category_spent_sum(self):
        pass  # TODO: Implement the category_spent_sum method (unnecessary)

    def payment_dict_sum(self, payment_list_dict):
        payment_sum = 0
        for payment in payment_list_dict:
            #print(f'''{payment["payment"]["name"]}: ''', payment["payment"]["spent"])
            payment_sum += payment["payment"]["spent"]
        print(f"payment sum: {payment_sum}")
        return payment_sum

    def get(self, request, **kwargs):
        dataset = self.graph_strap(request)
        num_colors = len(dataset)
        colors = self.generate_random_colors(num_colors)
        return render(request, self.template_name, context={"dataset": dataset, "colors": colors})
