from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_account.models import User
from app_order.forms import CreateOrderForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['mc_username', 'email', 'password1', 'password2']


class MCUsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mc_username']
        widgets = {
            'mc_username': forms.TextInput(attrs={
                'placeholder': 'Minecraft Username'
            })
        }


class OrderManagerForm(CreateOrderForm):
    class Meta(CreateOrderForm.Meta):
        fields = ['price', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('material', None)

        for field_name in list(self.fields.keys()):
            if field_name.startswith('enchantment_'):
                self.fields.pop(field_name)
