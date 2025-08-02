from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

from app_account.forms import UserRegisterForm


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the error below.")
        return render(request, 'account/register.html')
