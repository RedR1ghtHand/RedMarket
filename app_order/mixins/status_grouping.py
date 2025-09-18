from datetime import timedelta

from django.db.models import Case, IntegerField, Q, Value, When
from django.utils import timezone

from app_order.decorators import QueryTimer


class StatusGroupingMixin:
    """
    Mixin to provide status-based grouping for orders.
    Groups orders by user status: online, idle, offline.
    """

    def get_status_rank_annotation(self):
        return Case(
            When(
                Q(created_by__is_online=True) | 
                Q(created_by__last_seen_at__gte=timezone.now() - timedelta(minutes=5)),
                then=Value(0)
            ),
            When(
                Q(created_by__manual_status='idle') | 
                Q(created_by__last_seen_at__gte=timezone.now() - timedelta(minutes=15)),
                then=Value(1)
            ),
            default=Value(2),
            output_field=IntegerField(),
        )
    
    def apply_status_grouping(self, queryset):
        status_rank = self.get_status_rank_annotation()
        return queryset.annotate(status_rank=status_rank).order_by('status_rank')
    
    @QueryTimer("Status Grouping with Ordering")
    def apply_status_grouping_with_ordering(self, queryset, ordering_field=None):
        queryset = self.apply_status_grouping(queryset)
        
        if ordering_field:
            return queryset.order_by('status_rank', ordering_field)
        
        return queryset
        