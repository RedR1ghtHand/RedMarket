from django import forms
from django.contrib.auth.forms import UserCreationForm

from app_account.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['mc_username', 'email', 'password1', 'password2']
