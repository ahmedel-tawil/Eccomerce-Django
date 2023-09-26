from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from company.models import Company


# Create your models here.

# >>> for country in Incident.objects.get(title='Pavlova dispute').countries:
# ...     print(country.name)

class ShippingZone(models.Model):
    name = models.CharField(_('Shipping Zone'), max_length=100)
    country = CountryField(multiple=True)

    def __str__(self):
        return f'{self.name}'

    def get_zone_countries(self):
        countries = ShippingZone.objects.get(id=self.id).country
        return countries


class ShoppingRate(models.Model):
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE)
    rate_name = models.CharField(_('Rate Name'), max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    price = models.FloatField(_('Rate Price'), default=0)
    number_of_days = models.PositiveIntegerField(_('Number of Days'), default=1)

    def __str__(self):
        return f'{self.rate_name}'
