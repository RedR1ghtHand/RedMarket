from django import forms
from app_order.models import Order

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["price", "quantity"]
        widgets = {
            "price": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
        }
