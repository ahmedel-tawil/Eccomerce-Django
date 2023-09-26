import django_filters
from django import forms
from django_filters import CharFilter, ChoiceFilter, ModelChoiceFilter, BooleanFilter

from inventory.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    is_active = BooleanFilter(
        widget=forms.Select(choices=(('True', 'True'), ('False', 'False')),
                            attrs={"class": "form-control", 'onchange': 'this.form.submit()'}))
    category = ModelChoiceFilter(queryset=Category.objects.all(),
                                 widget=forms.Select(attrs={"class": "form-control", "onchange": 'this.form.submit()'}))

    class Meta:
        model = Product
        fields = ['category', 'is_active']
