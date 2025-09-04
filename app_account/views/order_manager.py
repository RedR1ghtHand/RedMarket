from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import ListView, UpdateView

from app_item.models import Category
from app_order.forms import CreateOrderForm
from app_order.models import Order, OrderEnchantment


class OrderManagerView(ListView):
    model = Order
    template_name = 'account/orders_manager/base.html'
    context_object_name = 'orders'
    paginate_by = 100

    @cached_property
    def _queryset(self):
        return (
            Order.objects.filter(created_by=self.request.user, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch(
                    'orderenchantment_set',
                    queryset=OrderEnchantment.objects.select_related('enchantment')
                )
            )
        )

    def get_queryset(self):
        return self._queryset

    def get_categories_queryset(self):
        return (
            Category.objects.filter(item_types__order__in=self._queryset)
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = self.get_categories_queryset()
        return context


class OrderCardUpdateView(UpdateView):
    model = Order
    form_class = CreateOrderForm
    template_name = 'account/orders_manager/_order_card_edit.html'
    
    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs['pk'], created_by=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['item_type'] = self.object.item_type
        return kwargs
    
    def form_valid(self, form):
        order = form.save()
        order.orderenchantment_set.all().delete()
        for enchantment, level in form.cleaned_data["enchantments"]:
            OrderEnchantment.objects.create(
                order=order,
                enchantment=enchantment,
                level=level
            )
        return HttpResponse(render_to_string('account/orders_manager/_order_card.html', 
                                           {'order': order}, request=self.request))


class OrderCardDeleteView(View):
    template_name = 'account/orders_manager/_order_card_delete.html'
    
    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs['pk'], created_by=self.request.user)
    
    def get(self, request, *args, **kwargs):
        order = self.get_object()
        return render(request, self.template_name, {'order': order})

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        category = order.item_type.category
        order.soft_delete()
        
        category_orders = Order.objects.filter(
            created_by=request.user,
            deleted_at__isnull=True,
            item_type__category=category
        ).prefetch_related(
            Prefetch(
                "orderenchantment_set",
                queryset=OrderEnchantment.objects.select_related("enchantment"),
            )
        )
        
        return HttpResponse(render_to_string(
            'account/orders_manager/_category_accordion.html',
            {'category': category, 'orders': category_orders},
            request=request
        ))
