from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import ListView

from app_account.forms import OrderUpdateForm
from app_item.models import Category
from app_order.models import Order, OrderEnchantment
from app_order.forms import CreateOrderForm

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


class OrderCardManagerView(View):
    template_name = "account/orders_manager/_order_card.html"
    edit_template_name = "account/orders_manager/_order_card_edit.html"
    delete_template_name = "account/orders_manager/_order_card_delete.html"

    def get_object(self, pk, user):
        return get_object_or_404(Order, pk=pk, created_by=user)

    def get(self, request, pk, *args, **kwargs):
        order = self.get_object(pk, request.user)

        partial = request.headers.get("HX-Request-Partial")

        if partial == "edit":
            form = CreateOrderForm(instance=order, item_type=order.item_type)
            html = render_to_string(
                self.edit_template_name,
                {"order": order, "form": form},
                request=request
            )
        elif partial == "delete":
            html = render_to_string(
                self.delete_template_name,
                {"order": order},
                request=request
            )
        else:
            html = render_to_string(self.template_name, {"order": order}, request=request)

        return HttpResponse(html)

    def post(self, request, pk, *args, **kwargs):
        order = self.get_object(pk, request.user)

        if "update_order" in request.POST:
            form = CreateOrderForm(request.POST, instance=order, item_type=order.item_type)
            if form.is_valid():
                order = form.save(commit=False)
                order.save()

                order.orderenchantment_set.all().delete()
                for enchantment, level in form.cleaned_data["enchantments"]:
                    OrderEnchantment.objects.create(
                        order=order,
                        enchantment=enchantment,
                        level=level
                    )

                messages.success(request, "Order updated.")
                html = render_to_string(self.template_name, {"order": order}, request=request)
            else:
                html = render_to_string(
                    self.edit_template_name,
                    {"order": order, "form": form},
                    request=request
                )
            return HttpResponse(html)

        elif "delete_order" in request.POST:
            category = order.item_type.category
            order.soft_delete()
            messages.success(request, "Order deleted.")

            category_orders = (
                Order.objects.filter(
                    created_by=request.user,
                    deleted_at__isnull=True,
                    item_type__category=category
                )
                .prefetch_related(
                    Prefetch(
                        "orderenchantment_set",
                        queryset=OrderEnchantment.objects.select_related("enchantment"),
                    )
                )
            )

            html = render_to_string(
                "account/orders_manager/_category_accordion.html",
                {"category": category, "orders": category_orders},
                request=request,
            )

            return HttpResponse(html)

        return redirect("order_manager")
