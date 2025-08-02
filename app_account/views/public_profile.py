from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from app_account.models import User
from app_item.models import Category
from app_order.mixins import OrdersSortingMixin
from app_order.models import Order, OrderEnchantment
from app_social.mixins import ReputationMixin


class PublicProfileView(ReputationMixin, OrdersSortingMixin, ListView):
    model = Order
    template_name = 'account/public_profile.html'
    context_object_name = 'orders'
    paginate_by = 5
    allowed_sort_fields = ['price', 'quantity']

    def dispatch(self, request, *args, **kwargs):
        self.public_user = get_object_or_404(User, mc_username=self.kwargs['mc_username'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (
            Order.objects
            .filter(created_by=self.public_user, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch('orderenchantment_set', queryset=OrderEnchantment.objects.select_related('enchantment'))
            )
            .order_by('-updated_at')
        )

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(item_type__category_id=category_id)

        return self.apply_ordering(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.request.GET.get('category')

        context.update({
            'public_user': self.public_user,
            'categories': Category.objects.all(),
            'selected_category': int(category_id) if category_id else None,
            'mc_server_wisper_command': settings.MC_SERVER_WISPER_COMMAND,
            'reputation_list': self.get_reputation_queryset(self.public_user),
        })

        context.update(self.get_sort_context())
        context.update(self.get_reputation_context(self.request, self.public_user))

        return context
