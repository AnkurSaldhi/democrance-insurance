from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import create_customer, create_quote, accept_quote, pay_quote, get_customer_policies,\
    get_policy_details, get_policy_history, search_customers

urlpatterns = [
    path('create_customer/', create_customer, name='create_customer'),
    path('create_quote/', create_quote, name='create_quote'),
    path('accept_quote/', accept_quote, name='accept_quote'),
    path('pay_quote/', pay_quote, name='pay_quote'),
    path('policies/', get_customer_policies, name='get_customer_policies'),
    path('policies/<int:quote_id>/', get_policy_details, name='get_policy_details'),
    path('policies/<int:quote_id>/history/', get_policy_history, name='get_policy_history'),
    path('search_customers/', search_customers, name='search_customers'),  # New endpoint for searching customers

]

if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
