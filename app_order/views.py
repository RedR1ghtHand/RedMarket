from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Prefetch
from formtools.wizard.views import SessionWizardView
from django.views.generic import ListView

from .models import Order, OrderEnchantment, ItemType, Material
from .forms import CreateOrderForm, SelectItemTypeForm
from .mixins import OrdersSortingMixin


class CreateOrderWizard(SessionWizardView):
    form_list = [
        ('select_item_type', SelectItemTypeForm),
        ('fill_order', CreateOrderForm),
    ]
    template_name = 'order/wts_wizard_form.html'

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        if step == 'fill_order':
            item_type_data = self.get_cleaned_data_for_step('select_item_type')
            if item_type_data and 'item_type' in item_type_data:
                kwargs['item_type'] = item_type_data['item_type']
        return kwargs

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        item_type_data = self.get_cleaned_data_for_step('select_item_type')
        context['selected_item_type'] = item_type_data['item_type'] if item_type_data else None
        return context

    def done(self, form_list, **kwargs):
        step_0_data = self.get_cleaned_data_for_step('select_item_type')
        step_1_data = self.get_cleaned_data_for_step('fill_order')

        order = Order.objects.create(
            created_by=self.request.user,
            item_type=step_0_data['item_type'],
            material=step_1_data.get('material', None),
            quantity=step_1_data['quantity'],
            price=step_1_data['price']
        )

        for enchantment, level in step_1_data.get('enchantments', []):
            OrderEnchantment.objects.create(
                order=order,
                enchantment=enchantment,
                level=level
            )
        return redirect('order_success')


def orders_view(request):
    item_type_id = request.GET.get('item_type')
    item_types = ItemType.objects.all().prefetch_related('materials')

    enriched_item_types = []
    for item in item_types:
        material_names = [mat.name.lower() for mat in item.materials.all()]
        enriched_item_types.append({
            'name': item.name,
            'slug': item.slug,
            'aliases': material_names
        })

    if item_type_id:
        orders = Order.objects.filter(item_type_id=item_type_id, deleted_at__isnull=True)[:10]
    else:
        orders = Order.objects.filter(deleted_at__isnull=True)[:10]

    return render(request, 'market.html', {
        'orders': orders,
        'item_types': item_types,
        'enriched_types': enriched_item_types,
        'selected_type': int(item_type_id) if item_type_id else None
    })


class OrderDetailView(OrdersSortingMixin, ListView):
    model = Order
    template_name = 'order/order_detail.html'
    paginate_by = 5
    allowed_sort_fields = ['price', 'quantity']

    def dispatch(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.item_type = get_object_or_404(ItemType, slug=self.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (
            Order.objects
            .filter(item_type=self.item_type, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch('orderenchantment_set', queryset=OrderEnchantment.objects.select_related('enchantment'))
            )
            .order_by('-updated_at')
        )

        # Material Filter
        material_filter = self.request.GET.get('material')
        if material_filter:
            queryset = queryset.filter(material__id=material_filter)

        return self.apply_ordering(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        material_filter = self.request.GET.get('material')

        context.update({
            'item_type': self.item_type,
            'materials': Material.objects.filter(applicable_to=self.item_type).values_list('id', 'name'),
            'selected_material': int(material_filter) if material_filter else None,
            'sort_fields': self.allowed_sort_fields,
            'item_types': ItemType.objects.all(),
            'selected_type': self.item_type,
            'mc_server_wisper_command': settings.MC_SERVER_WISPER_COMMAND,
        })

        context.update(self.get_sort_context())

        return context
