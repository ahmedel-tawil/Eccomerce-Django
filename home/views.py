from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from django_genericfilters.views import FilteredListView
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from home.filters import ProductFilter
from home.forms import ProductListForm
from inventory.models import *
from django.core import paginator
from django.template.loader import render_to_string

from vibgyor import settings


# Create your views here.
def home(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    category = Category.objects.all().filter(level=0)

    context = {

        'category': category,

    }
    return render(request, 'home/landing.html', context)


def shop(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    product = Product.objects.all()
    category = Category.objects.all()
    active_category = request.GET.get('category', '')
    if active_category:
        product = product.filter(category__slug=active_category)
    query = request.GET.get('query', '')
    url = request.path
    if query:
        product = product.filter(
            Q(name__icontains=query) | Q(description_s__icontains=query) | Q(category__name__icontains=query))

    context = {
        'productlist': product,
        'categories': category,
        'active_category': active_category,
        'url': url,

    }
    return render(request, 'home/shop.html', context)


class ProductList(ListView):
    model = Product
    template_name = 'home/shop.html'
    #   paginate_by = 6
    context_object_name = 'list'

    def get_queryset(self):
        product = Product.objects.all()
        category = Category.objects.all()
        active_category = self.request.GET.get('category', '')
        if active_category:
            product = product.filter(category__slug=active_category)
        # return Product.objects.all()
        queryset = {
            'productlist': product,
            'categories': category,
            'active_category': active_category}

        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return 'home/partials/product_list_items.html'
        return 'home/shop.html'

    # def get_context_data(self, *args, **kwargs):
    #     product = Product.objects.all()
    #     category = Category.objects.all()
    #     active_category = self.request.GET.get('category', '')
    #     if active_category:
    #         product = product.filter(category__slug=active_category)
    #     query = self.request.GET.get('query', '')
    #     url = self.request.path
    #
    #     context = {
    #         'categories': category,
    #         'active_category': active_category,
    #         'url': url,
    #     }
    #     return context


class ProductDetail(DetailView):
    template_name = 'home/shop-single.html'
    model = Product


def client_profile(request, slug):
    user = User.objects.get(slug=slug)
    orders = user.order_set.all()
    favourite_list = user.customerfavouriteitems_set.all()
    context = {
        'orders': orders,
        'favourite_list': favourite_list
    }
    return render(request, 'home/user-profile.html', context)
