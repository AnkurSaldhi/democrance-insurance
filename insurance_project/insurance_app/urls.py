from django.urls import path
from .views import create_customer, create_quote, accept_quote, pay_quote, get_customer_policies

urlpatterns = [
    path('create_customer/', create_customer, name='create_customer'),
    path('create_quote/', create_quote, name='create_quote'),
    path('accept_quote/', accept_quote, name='accept_quote'),
    path('pay_quote/', pay_quote, name='pay_quote'),
    path('policies/', get_customer_policies, name='get_customer_policies'),

]
