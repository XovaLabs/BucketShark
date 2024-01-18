from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from ...models import Category
from django.http import HttpResponseForbidden


class CategoryView(View, LoginRequiredMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/category.html'

    def get(self, request):
        category_records = Category.objects.filter(category_user=request.user)
        return render(request, self.template_name, {
            'category_records': category_records,
        })

    @staticmethod
    def post(request):
        print(request.POST)

        if 'add_new' in request.POST:
            new_category = Category(category_user=request.user, category_name='empty', category_privacy=True)
            new_category.save()

        return redirect('summary')
