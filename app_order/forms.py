from django import forms

from app_item.models import ItemType, Material
from .models import Order


class SelectItemTypeForm(forms.Form):
    item_type = forms.ModelChoiceField(
        queryset=ItemType.objects.all(),
        label='Select Item Type'
    )


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['material', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        item_type = kwargs.pop('item_type', None)
        super().__init__(*args, **kwargs)
        if item_type:
            materials_qs = Material.objects.filter(applicable_to=item_type)
            if materials_qs.exists():
                self.fields['material'] = forms.ModelChoiceField(
                    queryset=materials_qs,
                    required=False,
                    label="Material",
                    widget=forms.Select(attrs={'placeholder': 'Select Material'})
                )
            else:
                self.fields.pop('material', None)

            enchantments = item_type.enchantments.all()
            for enchantment in enchantments:
                field_name = f'enchantment_{enchantment.id}'
                self.fields[field_name] = forms.IntegerField(
                    label=f'{enchantment.name}',
                    min_value=1,
                    max_value=enchantment.max_level,
                    required=False,
                    widget=forms.NumberInput(attrs={
                        'placeholder': f'1-{enchantment.max_level}'
                    })
                )

