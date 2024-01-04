from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import View


class Logout(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('login')
