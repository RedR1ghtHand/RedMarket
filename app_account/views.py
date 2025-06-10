from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import ListView
from django.db.models import Prefetch
from django.conf import settings

from rest_framework import generics

from .models import User
from .forms import MCUsernameUpdateForm, OrderManagerForm
from .serializers import UserRegisterSerializer

from app_order.models import Order, OrderEnchantment
from app_item.models import Category
from app_social.mixins import ReputationMixin
from app_order.mixins import OrdersSortingMixin


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')  # redirect to account page
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account_view(request):
    return render(request, 'account/account.html', {'user': request.user})


@login_required
def account_settings_view(request):
    user = request.user

    mc_username_form = MCUsernameUpdateForm(request.POST or None, instance=user)
    pwd_form = PasswordChangeForm(user, request.POST or None)

    if 'update_mc_username' in request.POST and mc_username_form.is_valid():
        mc_username_form.save()
        messages.success(request, 'Minecraft username updated.')
        return redirect('user')

    if 'update_password' in request.POST and pwd_form.is_valid():
        pwd_form.save()
        update_session_auth_hash(request, pwd_form.user)
        messages.success(request, 'Password updated.')
        return redirect('user')

    return render(request, 'account/settings.html', {
        'mc_username_form': mc_username_form,
        'pwd_form': pwd_form,
    })


class AccountOrderManagerView(ListView):
    model = Order
    template_name = 'account/order_manager.html'
    context_object_name = 'orders'
    paginate_by = 100

    def get_queryset(self):
        user = self.request.user
        return (
            Order.objects.filter(created_by=user, deleted_at__isnull=True)
            .prefetch_related(
                Prefetch(
                    'orderenchantment_set',
                    queryset=OrderEnchantment.objects.select_related('enchantment')
                )
            )
        )

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('edit_order')
        if order_id:
            order_to_edit = get_object_or_404(Order, id=order_id, created_by=request.user)
            form = OrderManagerForm(instance=order_to_edit, item_type=order_to_edit.item_type)
            self.extra_context = {
                'order_to_edit': order_to_edit,
                'edit_form': form,
            }
        else:
            self.extra_context = {}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user

        if 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_edit = get_object_or_404(Order, id=order_id, created_by=user)
            form = OrderManagerForm(request.POST, instance=order_to_edit, item_type=order_to_edit.item_type)
            if form.is_valid():
                cleaned = form.cleaned_data
                form.save()
                # Handle enchantments logic if needed
                # order_to_edit.enchantments.clear()
                # for enchantment, level in cleaned.get('enchantments', []):
                #     OrderEnchantment.objects.create(order=order_to_edit, enchantment=enchantment, level=level)
                messages.success(request, 'Order updated.')
            else:
                messages.error(request, 'Failed to update order.')
            return redirect('order_manager')

        elif 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_delete = get_object_or_404(Order, id=order_id, created_by=user)
            order_to_delete.soft_delete()
            messages.success(request, 'Order deleted.')
            return redirect('order_manager')

        return redirect('order_manager')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context.update(self.extra_context)
        return context


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
