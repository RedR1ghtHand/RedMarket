from django.shortcuts import render
from django.views.generic import View

from app_item.models import ItemType
from app_order.forms import CreateOrderForm, SelectItemTypeForm
from app_order.models import Order, OrderEnchantment


class Step1SelectItemType(View):
    def get(self, request):
        form = SelectItemTypeForm()
        return render(request, "order/create_order/step1_select_type.html", {"form": form})

    def post(self, request):
        form = SelectItemTypeForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data["item_type"]
            create_form = CreateOrderForm(item_type=item_type)
            return render(request, "order/create_order/step2_fill_form.html", {
                "form": create_form,
                "item_type": item_type
            })
        return render(request, "order/create_order/step1_select_type.html", {"form": form})


class Step2SubmitOrder(View):
    def post(self, request):
        item_type_id = request.POST.get("item_type_id")
        item_type = ItemType.objects.get(id=item_type_id)
        form = CreateOrderForm(request.POST, item_type=item_type)
        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.create(
                created_by=request.user,
                item_type=item_type,
                material=cd.get("material"),
                quantity=cd["quantity"],
                price=cd["price"],
            )
            for enchantment, level in cd["enchantments"]:
                OrderEnchantment.objects.create(
                    order=order,
                    enchantment=enchantment,
                    level=level
                )
            return render(request, "order/create_order/order_success.html")
        return render(request, "order/create_order/step2_fill_form.html", {"form": form, "item_type": item_type})
