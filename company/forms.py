from django.forms import ModelForm
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from company.models import Company, Currency


class CompanyModelForm(ModelForm):
    class Meta:
        model = Company
        fields = ("is_active", "is_main", "is_shipping", "is_supplier", 'name', 'website',
                  'email', 'logo', 'business_type', 'description', 'facebook', 'twitter', 'linkedin', 'instagram',
                  'phone_number', 'address')
        widgets = {
            "is_active": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-dark-primary"),
            "is_main": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
            "is_shipping": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
            "is_supplier": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
        }
