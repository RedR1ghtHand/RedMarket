class OrdersSortingMixin:
    """
    Mixin to provide reusable ordering (sorting) logic for Django class-based views.
    Allows views to define `allowed_sort_fields` and automatically apply sorting
    based on GET parameters:sort=field&direction=asc|desc.
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
