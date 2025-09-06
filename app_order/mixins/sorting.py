from django.utils.functional import cached_property


class OrderSortingMixin:
    """
    Mixin to provide reusable ordering (sorting) logic for Django class-based views.
    Allows views to define `allowed_sort_fields` and automatically apply sorting
    based on GET parameters:sort=field&direction=asc|desc.
    """
    allowed_sort_fields = []

    @cached_property
    def sorting_context(self):
        return {
            "sort": self.request.GET.get("sort"),
            "direction": self.request.GET.get("direction", "asc"),
        }

    def get_ordering_params(self):
        sort = self.sorting_context["sort"]
        direction = self.sorting_context["direction"]

        if sort in self.allowed_sort_fields:
            if direction == 'desc':
                return f'-{sort}'
            elif direction == 'asc':
                return sort
            return None
        return None

    def apply_ordering(self, queryset):
        ordering = self.get_ordering_params()
        if ordering:
            return queryset.order_by(ordering)
        return queryset
