from django.contrib import admin

from currencies.forms import CurrencyModelForm
from currencies.models import Currency


# Register your models here.
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", 'code', "is_active", "is_base", "is_default", "symbol", "factor")
    list_filter = ("is_active",)
    search_fields = ("name", "code")
    form = CurrencyModelForm


admin.site.register(Currency, CurrencyAdmin)
