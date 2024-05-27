from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
import json
from django.http import JsonResponse
from ...models import Category


class CategoryClass(LoginRequiredMixin, View):

    def post(self, request):
        data = json.loads(request.body)
        category_name = data.get('category_name')
        if category_name:
            new_category = Category.objects.create(
                category_name=category_name,
                category_user=request.user
            )
            return JsonResponse({
                'success': True,
                'category_name': new_category.category_name,
                'category_id': new_category.category_id
            })
        return JsonResponse({'success': False})
