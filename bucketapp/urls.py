from django.urls import path
from . import views
from .views import Home, LoginClass, SignUpClass, Logout, PaymentView, CategoryClass


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LoginClass.as_view(), name='login'),
    path('signup/', SignUpClass.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),
    path('payments/', PaymentView.as_view(), name='payment_view'),
    path('create_category/', CategoryClass.as_view(), name='create_category'),
]
