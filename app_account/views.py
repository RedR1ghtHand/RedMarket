from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework import generics

from .models import User
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


