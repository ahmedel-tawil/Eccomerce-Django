from django.forms import ModelForm
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from currencies.models import Currency


class CurrencyModelForm(ModelForm):
    class Meta:
        model = Currency
        fields = ("is_active", "is_base", "is_default", 'name',
                  'symbol', 'factor'
                  )
        widgets = {
            "is_active": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-dark-primary"),
            "is_base": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
            "is_default": DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
        }
