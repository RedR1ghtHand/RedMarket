from app_order.forms import CreateOrderForm


class OrderManagerForm(CreateOrderForm):
    class Meta(CreateOrderForm.Meta):
        fields = ['price', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('material', None)

        for field_name in list(self.fields.keys()):
            if field_name.startswith('enchantment_'):
                self.fields.pop(field_name)
