import json

from django.db.models import Sum

from company.models import User
from inventory.models import Category
from .models import Order, CustomerFavouriteItems


def order_context(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            return {'order': order}
        except:
            return {}

    return {}


def fav_context(request):
    if request.user.is_authenticated:
        try:
            favourite = CustomerFavouriteItems.objects.filter(user=request.user)
            return {'favourite': favourite}
        except:
            return {}

    return {}


def order_stat_context(request):
    order_total = Order.objects.all()
    total_sales = Order.objects.filter(ordered=True).values('items__size__product_price').aggregate(
        Sum('items__size__product_price'))['items__size__product_price__sum']
    total_sales_by_catg = Order.objects.filter(ordered=True).values('items__product__category__name',
                                                                    'items__product__category__image', ).order_by(
        'items__product__category__name').annotate(sum=Sum('items__size__product_price'))

    order_to_ship = Order.objects.filter(ordered=True, order_transit=False).order_by('ordered_date')[:6]
    context = {
        'order_total': order_total,
        'total_sales': total_sales,
        'total_sales_by_catg': total_sales_by_catg,
        # 'category': category,

        'order_to_ship': order_to_ship,
    }
    return context


def total_sales_growth(request):
    total_sales = Order.objects.filter(ordered=True).values('items__size__product_price').aggregate(
        Sum('items__size__product_price'))['items__size__product_price__sum']
    context = {
        'total_company_sales': total_sales,
    }
    return context


def total_profit(request):
    total_sales = Order.objects.filter(ordered=True).values('items__size__product_price').aggregate(
        Sum('items__size__product_price'))['items__size__product_price__sum']

    total_cost = Order.objects.filter(ordered=True).values('items__size__product_price').aggregate(
        Sum('items__size__price'))['items__size__price__sum']
    profit = total_sales - total_cost

    context = {
        'total_company_sales': total_sales,
        'total_cost': total_cost,
        'profit': profit,
    }
    return context


def order_stat_data(request):
    total_sales_by_catg = Order.objects.filter(ordered=True).values('items__product__category__name', ).order_by(
        'items__product__category__name').annotate(sum=Sum('items__size__product_price'))
    labels = []
    data = []
    for qs in total_sales_by_catg:
        labels.append(qs['items__product__category__name'])
        data.append(qs['sum'])

    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),

    }
    return context
