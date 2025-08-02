from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from app_account.forms import MCUsernameUpdateForm


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account_view(request):
    return render(request, 'account/user_profile.html', {'user': request.user})


@login_required
def account_settings_view(request):
    user = request.user

    mc_username_form = MCUsernameUpdateForm(request.POST or None, instance=user)
    pwd_form = PasswordChangeForm(user, request.POST or None)

    if 'update_mc_username' in request.POST and mc_username_form.is_valid():
        mc_username_form.save()
        messages.success(request, 'Minecraft username updated.')

        return redirect('settings')

    if 'update_password' in request.POST and pwd_form.is_valid():
        pwd_form.save()
        update_session_auth_hash(request, pwd_form.user)
        messages.success(request, 'Password updated.')

        return redirect('settings')

    return render(request, 'account/settings.html', {
        'mc_username_form': mc_username_form,
        'pwd_form': pwd_form,
    })
