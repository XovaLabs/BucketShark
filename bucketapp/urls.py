from django.urls import path
from .views import (Home, LoginClass, SignUpClass, Logout, PaymentView, CategoryClass, OneTimePaymentView,
                    RepeatedPaymentView, CategoryView)


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LoginClass.as_view(), name='login'),
    path('signup/', SignUpClass.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),
    path('payments/', PaymentView.as_view(), name='payment_view'),
    path('create_category/', CategoryClass.as_view(), name='create_category'),
    path('payments/onetime/', OneTimePaymentView.as_view(), name='add_onetime_payment'),
    path('payments/repeated/', RepeatedPaymentView.as_view(), name='add_repeated_payment'),
    path('dashboard/summary/', CategoryView.as_view(), name='summary'),
    # path('dashboard/'),
]
