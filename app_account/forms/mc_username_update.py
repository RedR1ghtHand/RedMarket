from django import forms

from app_account.models import User


class MCUsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mc_username']
        widgets = {
            'mc_username': forms.TextInput(attrs={
                'placeholder': 'Minecraft Username'
            })
        }
