from django.urls import reverse
from django.utils.functional import cached_property

from app_item.models import ItemType


class EnrichedItemTypeMixin:
    """
    Mixin to provide enriched item type data for views.
    Includes item type name, slug, URL, material aliases, and material ID mapping.
    Useful for search bars and filtering logic in templates.
    """
    @cached_property
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

        return enriched, item_types
