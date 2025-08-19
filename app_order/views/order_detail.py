import json

from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import ListView

from app_item.models import ItemType, Material
from app_order.mixins import OrderSortingMixin, EnrichedItemTypeMixin, OrderFilteringMixin
from app_order.models import Order, OrderEnchantment


class OrderDetailView(OrderSortingMixin, OrderFilteringMixin, EnrichedItemTypeMixin, ListView):
    model = Order
    template_name = 'order/detail_page/base.html'
    context_object_name = 'orders'
    paginate_by = 10
    allowed_sort_fields = ['price', 'quantity']

    @property
    def slug(self):
        return self.kwargs.get('slug')

    @cached_property
    def item_type(self):
        slug = self.slug
        if not slug:
            raise ValueError("slug is required for resolving item_type")
        return get_object_or_404(ItemType, slug=slug)

    @cached_property
    def materials(self):
        return list(Material.objects.filter(applicable_to=self.item_type).values_list('id', 'name'))

    def get_queryset(self):
        queryset = (
            Order.objects
            .filter(item_type=self.item_type, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch('orderenchantment_set', queryset=OrderEnchantment.objects.select_related('enchantment'))
            )
            .order_by('-updated_at')
        )

        queryset = self.apply_filters(queryset)
        return self.apply_ordering(queryset)

    def get_htmx_template(self, partial):
        partial_templates = {
            "body": "order/detail_page/_body.html",
            "table": "order/detail_page/_orders_table.html",
            "rows": "order/detail_page/_table_rows.html"
        }
        return partial_templates.get(partial, self.template_name)

    def get_template_names(self):
        if self.request.htmx:
            return [self.get_htmx_template(self.request.headers.get("HX-Request-Partial"))]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'item_type': self.item_type,
            'materials': self.materials,
            'selected_material': int(self.filter_context["material"]) if self.filter_context["material"] else None,
            'enchantment_filter': self.filter_context["enchantments"],
            'sort_fields': self.allowed_sort_fields,
            'current_sort': self.sorting_context["sort"],
            'current_direction': self.sorting_context["direction"],
            'item_types': ItemType.objects.all(),
            'mc_server_wisper_command': settings.MC_SERVER_WISPER_COMMAND,
            'enriched_types_json': json.dumps(self.get_enriched_item_types())
        })

        return context
