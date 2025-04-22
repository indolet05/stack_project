from django import forms
from django.core.validators import MinValueValidator

class CartAddItemForm(forms.Form):
    quantity = forms.IntegerField(
        initial=1,
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={
            'min': 1,
            'class': 'quantity-input'
        })
    )