from django.shortcuts import render
from django.views.generic import View


class Home(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'bucketapp/home.html'

    def get(self, request):
        return render(request, self.template_name)

