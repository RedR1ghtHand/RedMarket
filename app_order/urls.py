from django.http import HttpResponse
from django.urls import path
from .views import CreateOrderWizard, orders_view, OrderDetailView
from .forms import CreateOrderForm, SelectItemTypeForm

order_forms = [CreateOrderForm, SelectItemTypeForm]

urlpatterns = [
    path('create/', CreateOrderWizard.as_view(), name='create_order'),
    path('success/', lambda request: HttpResponse("Order created successfully!"), name='order_success'),
    path('market/', orders_view, name='orders'),
    path('orders/detail/<slug:slug>/', OrderDetailView.as_view(), name='order_detail')
]
