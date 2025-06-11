from django.http import HttpResponse
from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import CreateOrderWizard, MarketView, OrderDetailView
from .forms import CreateOrderForm, SelectItemTypeForm

order_forms = [CreateOrderForm, SelectItemTypeForm]

urlpatterns = [
    path('create/', login_required(CreateOrderWizard.as_view()), name='create_order'),
    path('success/', lambda request: HttpResponse("Order created successfully!"), name='order_success'),
    path('market/', MarketView.as_view(), name='orders'),
    path('detail/<slug:slug>/', OrderDetailView.as_view(), name='order_detail')
]
