from django import forms

from app_account.models import User
from app_order.forms import CreateOrderForm


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
        # Don't pass item_type — or override logic to skip extra fields
        super().__init__(*args, **kwargs)
        # Remove anything dynamically added from parent
        self.fields.pop('material', None)

        for field_name in list(self.fields.keys()):
            if field_name.startswith('enchantment_'):
                self.fields.pop(field_name)
