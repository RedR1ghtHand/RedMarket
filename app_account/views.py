from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Prefetch
from django.conf import settings

from rest_framework import generics

from .models import User
from app_order.models import Order, OrderEnchantment
from app_item.models import Category
from .forms import MCUsernameUpdateForm, OrderManagerForm
from app_order.forms import CreateOrderForm
from .serializers import UserRegisterSerializer


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


def account_order_manager_view(request):
    user = request.user
    orders = Order.objects.filter(created_by=user, deleted_at__isnull=True)
    orders = orders.prefetch_related(
        Prefetch(
            'orderenchantment_set',
            queryset=OrderEnchantment.objects.select_related('enchantment')
        )
    )
    order_to_edit = None
    form = None

    if request.method == 'POST':
        if 'edit_order' in request.POST:
            order_id = request.POST.get('edit_order')
            order_to_edit = get_object_or_404(Order, id=order_id, created_by=user)
            form = OrderManagerForm(instance=order_to_edit, item_type=order_to_edit.item_type)

        elif 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_edit = get_object_or_404(Order, id=order_id, created_by=user)
            form = OrderManagerForm(request.POST, instance=order_to_edit, item_type=order_to_edit.item_type)
            if form.is_valid():
                cleaned = form.cleaned_data
                form.save()
                # order_to_edit.enchantments.clear()
                # for enchantment, level in cleaned.get('enchantments', []):
                #     OrderEnchantment.objects.create(order=order_to_edit, enchantment=enchantment, level=level)
            return redirect('order_manager')

        elif 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_delete = get_object_or_404(Order, id=order_id, created_by=user)
            order_to_delete.soft_delete()
            messages.success(request, 'Order deleted.')
            return redirect('order_manager')

        else:
            form = None

    return render(request, 'account/order_manager.html', {
        'user': request.user,
        'orders': orders,
        'edit_form': form,
        'order_to_edit': order_to_edit
    })


def account_public_profile_view(request, mc_username):
    public_user = get_object_or_404(User, mc_username=mc_username)
    orders = Order.objects.filter(created_by=public_user, deleted_at__isnull=True)

    sort_fields = ['price', 'quantity']
    sort = request.GET.get('sort', 'price')
    direction = request.GET.get('direction', 'asc')

    if sort in sort_fields:
        ordering = sort if direction == 'asc' else f'-{sort}'
        orders = orders.order_by(ordering)

    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        orders = orders.filter(item_type__category_id=category_id)

    return render(request, 'account/public_profile.html', {
        'public_user': public_user,
        'orders': orders,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'current_sort': sort,
        'current_direction': direction,
        'mc_server_wisper_command': settings.MC_SERVER_WISPER_COMMAND,
    })
