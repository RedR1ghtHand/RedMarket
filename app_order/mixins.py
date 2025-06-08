from django.urls import reverse

from app_item.models import ItemType


class OrdersSortingMixin:
    """
   Mixin to provide reusable ordering (sorting) logic for Django class-based views.
   Allows views to define `allowed_sort_fields` and automatically apply sorting
   based on GET parameters: ?sort=field&direction=asc|desc.
   """
    allowed_sort_fields = []

    def get_ordering_params(self):
        sort = self.request.GET.get('sort')
        direction = self.request.GET.get('direction', 'asc')

        if sort in self.allowed_sort_fields:
            return sort if direction == 'asc' else f'-{sort}'
        return None

    def apply_ordering(self, queryset):
        ordering = self.get_ordering_params()
        if ordering:
            return queryset.order_by(ordering)
        return queryset

    def get_sort_context(self):
        return {
            'current_sort': self.request.GET.get('sort'),
            'current_direction': self.request.GET.get('direction', 'asc'),
        }


class EnrichedItemTypeMixin:
    """
    Mixin to provide enriched item type data for views.
    Includes item type name, slug, URL, material aliases, and material ID mapping.
    Useful for search bars and filtering logic in templates.
    """
    def get_enriched_item_types(self):
        item_types = ItemType.objects.all().prefetch_related('materials')
        enriched = []

        for item in item_types:
            materials = item.materials.all()
            material_names = [mat.name.lower() for mat in materials]
            material_map = {mat.name: mat.id for mat in materials}

            enriched.append({
                'name': item.name,
                'slug': item.slug,
                'url': reverse('order_detail', args=[item.slug]),
                'aliases': material_names,
                'material_map': material_map,
            })

        return enriched
