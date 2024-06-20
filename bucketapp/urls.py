from django.urls import path
from .views import (Home, LoginClass, SignUpClass, Logout, PaymentView, OneTimePaymentView,
                    RepeatedPaymentView, CategoryView, Dashboard)

urlpatterns = [
    path('login/', LoginClass.as_view(), name='login'),
    path('signup/', SignUpClass.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),

    #   TODO: Fix this view OR DELETE VIEW. The one below.
    path('payments/', PaymentView.as_view(), name='payment_view'),

    path('payments/onetime/', OneTimePaymentView.as_view(), name='add_onetime_payment'),
    path('payments/repeated/', RepeatedPaymentView.as_view(), name='add_repeated_payment'),
    path('dashboard/summary/', CategoryView.as_view(), name='summary'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
]
