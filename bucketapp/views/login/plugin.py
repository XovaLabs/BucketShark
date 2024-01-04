from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View


class LoginClass(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to the home page

        form = AuthenticationForm()
        return render(request, 'bucketapp/login.html', {'form': form})

    @staticmethod
    def post(request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Session is created here
                return redirect('home')  # Redirect to a success page.
            else:
                # Invalid login
                return render(request, 'login.html', {'form': form})
        return render(request, 'bucketapp/login.html', {'form': form})
