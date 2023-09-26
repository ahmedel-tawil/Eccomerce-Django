from django import forms
from django_genericfilters.forms import FilteredForm
from django.utils.translation import gettext_lazy as _


class ProductListForm(FilteredForm):
    query = forms.CharField(label=_('Query'), required=False)

    priority = forms.ChoiceField(label=_('Priority'),
                                 required=False,
                                 choices=(
                                     ('0', 'High'),
                                     ('1', 'Normal'),
                                     ('2', 'Low')
                                 ))

    def get_order_by_choices(self):
        return [('created_date', _(u'date joined')),
                ('updated_at', _(u'last login')),
                ]
