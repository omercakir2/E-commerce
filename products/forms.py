from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
