from django import forms

from app_item.models import ItemType, Material, Enchantment
from app_order.models import Order


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

            existing = {}
            if self.instance.pk:
                existing = {
                    e.enchantment_id: e.level
                    for e in self.instance.orderenchantment_set.all()
                }
            self.enchantment_fields = []

            for enchantment in item_type.enchantments.all():
                self.fields[str(enchantment.id)] = forms.IntegerField(
                    label=enchantment.name,
                    min_value=1,
                    max_value=enchantment.max_level,
                    required=False,
                    initial=existing.get(enchantment.id, None),
                    widget=forms.NumberInput(attrs={'placeholder': f'1-{enchantment.max_level}'})
                )
                self.fields[str(enchantment.id)].is_enchantment = True
                self.enchantment_fields.append(enchantment)

    def clean(self):
        cleaned_data = super().clean()
        enchantments = []

        for enchantment in getattr(self, 'enchantment_fields', []):
            level = cleaned_data.get(str(enchantment.id))
            if level:
                enchantments.append((enchantment, level))

        cleaned_data['enchantments'] = enchantments
        return cleaned_data
