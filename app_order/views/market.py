import json

from django.views.generic import TemplateView

from app_item.models import ItemType
from app_order.mixins import EnrichedItemTypeMixin
from app_order.models import Order


class MarketView(EnrichedItemTypeMixin, TemplateView):
    template_name = 'market.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.filter(deleted_at__isnull=True)[:10]

        context.update({
            'orders': orders,
            'item_types': ItemType.objects.all(),
            'enriched_types_json': json.dumps(self.get_enriched_item_types()),
        })
        return context
