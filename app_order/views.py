from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from formtools.wizard.views import SessionWizardView

from .models import Order, OrderEnchantment, ItemType, Material
from .forms import CreateOrderForm, SelectItemTypeForm


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
        orders = Order.objects.filter(item_type_id=item_type_id, deleted_at__isnull=True).order_by('-created_at')[:10]
    else:
        orders = Order.objects.filter(deleted_at__isnull=True).order_by('-created_at')[:10]

    return render(request, 'market.html', {
        'orders': orders,
        'item_types': item_types,
        'enriched_types': enriched_item_types,
        'selected_type': int(item_type_id) if item_type_id else None
    })


def order_detail_view(request, slug):
    item_type = get_object_or_404(ItemType, slug=slug)
    all_orders = Order.objects.filter(item_type=item_type, deleted_at__isnull=True).order_by('-updated_at')
    all_orders = all_orders.prefetch_related(
        Prefetch(
            'orderenchantment_set',
            queryset=OrderEnchantment.objects.select_related('enchantment')
        )
    )

    sort_fields = ['price', 'quantity']
    sort = request.GET.get('sort')
    direction = request.GET.get('direction', 'asc')
    material_filter = request.GET.get('material')
    item_types = ItemType.objects.all()
    selected_type = get_object_or_404(ItemType, slug=slug)

    if sort in sort_fields:
        ordering = sort if direction == 'asc' else f"-{sort}"
        all_orders = all_orders.order_by(ordering)

    if material_filter:
        all_orders = all_orders.filter(material__id=material_filter)

    materials = Material.objects.filter(applicable_to=item_type).values_list('id', 'name')

    paginator = Paginator(all_orders, 5)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'item_type': item_type,
        'orders': orders,
        'current_sort': sort,
        'current_direction': direction,
        'sort_fields': sort_fields,
        'materials': materials,
        'selected_material': int(material_filter) if material_filter else None,
        'item_types': item_types,
        'selected_type': selected_type,
        'mc_server_wisper_command': settings.MC_SERVER_WISPER_COMMAND,
        'paginator': paginator
    }
    return render(request, 'order/order_detail.html', context)
