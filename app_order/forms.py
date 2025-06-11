from django import forms

from app_item.models import ItemType, Material, Enchantment
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
                    required=True,
                    label="Material",
                    empty_label=None
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
                    widget=forms.NumberInput(attrs={'placeholder': f'1-{enchantment.max_level}'})
                )

    def clean(self):
        cleaned_data = super().clean()
        enchantments = []

        for field_name in self.fields:
            if field_name.startswith('enchantment_'):
                level = cleaned_data.get(field_name)
                if level:
                    enchantment_id = int(field_name.replace('enchantment_', ''))
                    try:
                        enchantment = Enchantment.objects.get(id=enchantment_id)
                        enchantments.append((enchantment, level))
                    except Enchantment.DoesNotExist:
                        pass

        cleaned_data['enchantments'] = enchantments
        return cleaned_data

