from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView

from app_account.forms import OrderManagerForm
from app_order.models import Order, OrderEnchantment


class OrderManagerView(ListView):
    model = Order
    template_name = 'account/order_manager.html'
    context_object_name = 'orders'
    paginate_by = 100

    def get_queryset(self):
        user = self.request.user
        return (
            Order.objects.filter(created_by=user, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch(
                    'orderenchantment_set',
                    queryset=OrderEnchantment.objects.select_related('enchantment')
                )
            )
        )

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('edit_order')
        if order_id:
            order_to_edit = get_object_or_404(Order, id=order_id, created_by=request.user)
            form = OrderManagerForm(instance=order_to_edit, item_type=order_to_edit.item_type)
            self.extra_context = {
                'order_to_edit': order_to_edit,
                'edit_form': form,
            }
        else:
            self.extra_context = {}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user

        if 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_edit = get_object_or_404(Order, id=order_id, created_by=user)
            form = OrderManagerForm(request.POST, instance=order_to_edit, item_type=order_to_edit.item_type)
            if form.is_valid():
                cleaned = form.cleaned_data
                form.save()
                # Handle enchantments logic if you need
                # order_to_edit.enchantments.clear()
                # for enchantment, level in cleaned.get('enchantments', []):
                #     OrderEnchantment.objects.create(order=order_to_edit, enchantment=enchantment, level=level)
                messages.success(request, 'Order updated.')
            else:
                messages.error(request, 'Failed to update order.')
            return redirect('order_manager')

        elif 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_delete = get_object_or_404(Order, id=order_id, created_by=user)
            order_to_delete.soft_delete()
            messages.success(request, 'Order deleted.')
            return redirect('order_manager')

        return redirect('order_manager')
