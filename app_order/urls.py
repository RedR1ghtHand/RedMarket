from django.http import HttpResponse
from django.urls import path

from .forms import CreateOrderForm, SelectItemTypeForm
from .views import MarketView, OrderDetailView, Step1SelectItemType, Step2SubmitOrder

order_forms = [CreateOrderForm, SelectItemTypeForm]

urlpatterns = [
    path("create/", Step1SelectItemType.as_view(), name="select_item_type"),
    path("create/submit/", Step2SubmitOrder.as_view(), name="submit_order"),
    path('success/', lambda request: HttpResponse("Order created successfully!"), name='order_success'),
    path('market/', MarketView.as_view(), name='orders'),
    path('detail/<slug:slug>/', OrderDetailView.as_view(), name='order_detail')
]
