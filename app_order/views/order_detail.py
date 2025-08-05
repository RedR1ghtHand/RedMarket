import json

from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from app_item.models import ItemType, Material
from app_order.mixins import OrdersSortingMixin, EnrichedItemTypeMixin
from app_order.models import Order, OrderEnchantment


class OrderDetailView(OrdersSortingMixin, EnrichedItemTypeMixin, ListView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'orders'
    paginate_by = 10
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

        material_filter = self.request.GET.get('material')
        if material_filter:
            queryset = queryset.filter(material__id=material_filter)

        enchantment_filter = self.request.GET.getlist("enchantments")
        if enchantment_filter :
            queryset = queryset.filter(enchantments__id__in=enchantment_filter ).distinct()

        return self.apply_ordering(queryset)

    def get_template_names(self):
        if self.request.htmx:
            if self.request.headers.get("HX-Request-Partial") == "table":
                return ["order/order_table_partial.html"]
            elif self.request.headers.get("HX-Request-Partial") == "rows":
                return ["order/order_table_rows.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        material_filter = self.request.GET.get('material')
        enchantment_filter = self.request.GET.getlist("enchantments")

        context.update({
            'item_type': self.item_type,
            'materials': Material.objects.filter(applicable_to=self.item_type).values_list('id', 'name'),
            'selected_material': int(material_filter) if material_filter else None,
            'enchantment_filter': enchantment_filter,
            'sort_fields': self.allowed_sort_fields,
            'item_types': ItemType.objects.all(),
            'mc_server_wisper_command': settings.MC_SERVER_WISPER_COMMAND,
            'enriched_types_json': json.dumps(self.get_enriched_item_types())
        })

        context.update(self.get_sort_context())

        return context
