from django import template
from sales.models import Order, CustomerFavouriteItems

register = template.Library()


@register.filter
def favourite_item_count(user):
    if user.is_authenticated:
        qs = CustomerFavouriteItems.objects.filter(user=user)
        if qs.exists():
            return qs.count()
    return 0
