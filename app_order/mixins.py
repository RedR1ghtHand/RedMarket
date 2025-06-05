class OrdersSortingMixin:
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