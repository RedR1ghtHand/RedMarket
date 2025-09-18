from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.utils.functional import cached_property


class OrderFilteringMixin:
    """
    Combines material and enchantment filtering logic.
    Provides filter application methods and context-friendly filter data.
    """

    def filter_by_material(self, queryset):
        if self.filter_context["material"]:
            queryset = queryset.filter(material__id=self.filter_context["material"])
        return queryset

    def filter_by_enchantments(self, queryset):
        enchantments_filter = self.request.GET.getlist("enchantments")
        try:
            enchantments_ids = list(map(int, enchantments_filter))
        except ValueError:
            raise ValidationError("Enchantment IDs must be integers.")
        if enchantments_ids:
            queryset = queryset.filter(enchantments__id__in=enchantments_ids)
            queryset = queryset.annotate(
                matched_enchantments=Count(
                    'enchantments',
                    filter=Q(enchantments__id__in=enchantments_ids),
                    distinct=True
                )
            ).filter(matched_enchantments=len(enchantments_ids))
        return queryset

    def apply_filters(self, queryset):
        queryset = self.filter_by_material(queryset)
        queryset = self.filter_by_enchantments(queryset)
        return queryset

    @cached_property
    def filter_context(self):
        return {
            "material": self.request.GET.get("material"),
            "enchantments": self.request.GET.getlist("enchantments"),
        }


class OrderCategoryFilterMixin:
    @cached_property
    def filter_context(self):
        return {
            "category": self.request.GET.get("category")
        }

    def filter_by_category(self, queryset):
        category = self.filter_context["category"]
        if category:
            queryset = queryset.filter(item_type__category__id=category)
        return queryset