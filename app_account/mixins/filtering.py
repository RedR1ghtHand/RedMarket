from django.utils.functional import cached_property


class CategoryFilterMixin:
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
