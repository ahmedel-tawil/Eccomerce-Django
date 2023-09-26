from django.contrib import admin

from company.models import Company
from .models import ShippingZone, ShoppingRate


# Register your models here.

class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_zone_countries')


admin.site.register(ShippingZone, ShippingZoneAdmin)


class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ('rate_name', 'company', 'zone', 'price', 'number_of_days')

    list_filter = ('company', 'zone__country')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['company'].queryset = Company.objects.filter(is_shipping=True)
        return super(ShippingRateAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(ShoppingRate, ShippingRateAdmin)
