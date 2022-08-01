from django import forms

from .models import Customer


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__()
        for field in self.fields.values():
            field.widget = forms.widgets.TextInput(attrs={
                'class': 'form-control',
            })

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'city', 'phone_number', 'email', 'address')
