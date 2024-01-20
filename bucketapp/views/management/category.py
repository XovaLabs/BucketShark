from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from ...models import Category
from django.http import HttpResponseForbidden


class CategoryView(View, LoginRequiredMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/category.html'

        #  function mapping
        self.function_mapping = {"save": self.save_category,
                                 "add_new": self.add_new_category,
                                 "delete": self.delete_category,
                                 }

    def save_category(self, request):
        print("saved")
        record = Category.objects.get(pk=request.POST['id'])
        record.category_name = request.POST['name']
        record.budgeted = request.POST['budgeted']
        record.save()

    def add_new_category(self, request):
        new_category = Category(category_user=request.user, category_name='empty',
                                category_privacy=True)
        new_category.save()

    def delete_category(self, request):
        print("deleted")
        record = Category.objects.get(pk=request.POST['id'])
        record.delete()

    def get(self, request):
        category_records = Category.objects.filter(category_user=request.user)
        return render(request, self.template_name, {
            'category_records': category_records,
        })

    def post(self, request):
        print(request.POST)

        self.function_mapping[request.POST['submit']](request)
        return redirect('summary')
