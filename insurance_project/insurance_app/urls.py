from django.urls import path
from .views import create_customer, create_quote, accept_quote, pay_quote

urlpatterns = [
    path('create_customer/', create_customer, name='create_customer'),
    path('create_quote/', create_quote, name='create_quote'),  # Endpoint for creating a quote
    path('accept_quote/', accept_quote, name='accept_quote'),
    path('pay_quote/', pay_quote, name='pay_quote'),  # Endpoint for paying a quote
]
