from django import forms
from .models import ProductModel, CategoryModel, TagModel, OrderModel
from modules.models import AddressModel
from django.forms import ModelForm, TextInput

class ProductForm(forms.ModelForm):
    """
    Form to create products
    """
    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'image','description', 'company', 'street', 'city', 'state', 'country', 'pin_code', 'latitude', 'longitude'  ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['ordered_by',   'email', 'mobile_number', 'total_amount', 'quantity', 'street', 'city', 'state', 'country', 'pin_code', 'latitude', 'longitude']


class CartOrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['ordered_by',   'email', 'mobile_number', 'street', 'city', 'state', 'country', 'pin_code', 'latitude', 'longitude']
