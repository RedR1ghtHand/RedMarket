from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import ListView

from app_account.mixins import CategoryFilterMixin
from app_account.models import User
from app_item.models import Category
from app_order.mixins import OrderSortingMixin
from app_order.models import Order, OrderEnchantment
from app_social.mixins import ReputationMixin


class PublicProfileView(
    ReputationMixin, OrderSortingMixin, CategoryFilterMixin, ListView
):
    model = Order
    template_name = "account/public_profile/base.html"
    context_object_name = "orders"
    paginate_by = 10
    allowed_sort_fields = ["price", "quantity"]

    @property
    def mc_username(self):
        return self.kwargs["mc_username"]

    @cached_property
    def public_user(self):
        user = self.mc_username
        if not user:
            raise ValueError(
                "User mc_username is required for resolving public profile"
            )
        return get_object_or_404(User, mc_username=user)

    @cached_property
    def categories(self):
        return list(Category.objects.all().values_list("id", "name"))

    def get_queryset(self):
        queryset = (
            Order.objects.filter(created_by=self.public_user, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch(
                    "orderenchantment_set",
                    queryset=OrderEnchantment.objects.select_related("enchantment"),
                )
            )
            .order_by("-updated_at")
        )

        queryset = self.filter_by_category(queryset)
        return self.apply_ordering(queryset)

    def get_htmx_template(self, partial):
        partial_templates = {
            "body": "account/public_profile/_body.html",
            "table": "account/public_profile/_orders_table.html",
            "rows": "account/public_profile/_table_rows.html",
        }
        return partial_templates.get(partial, self.template_name)

    def get_template_names(self):
        if self.request.htmx:
            return [
                self.get_htmx_template(self.request.headers.get("HX-Request-Partial"))
            ]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "public_user": self.public_user,
                "categories": self.categories,
                "selected_category": (
                    int(self.filter_context["category"])
                    if self.filter_context["category"]
                    else None
                ),
                "current_sort": self.sorting_context["sort"],
                "current_direction": self.sorting_context["direction"],
                "mc_server_wisper_command": settings.MC_SERVER_WISPER_COMMAND,
            }
        )

        context.update(self.get_reputation_context(self.request, self.public_user))

        return context
