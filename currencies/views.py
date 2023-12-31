from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from .models import Currency
from .conf import SESSION_KEY


def _is_safe_url(url, allowed_hosts, **kwargs):
    return url_has_allowed_host_and_scheme(url, allowed_hosts=allowed_hosts, **kwargs)


@never_cache
def set_currency(request):
    next, currency_code = (
        request.POST.get('next') or request.GET.get('next'),
        request.POST.get('currency_code', None) or
        request.GET.get('currency_code', None))
    #
    # if not _is_safe_url(next, [request.get_host()]):
    #     next = request.META.get('HTTP_REFERER')
    #     if not _is_safe_url(next, [request.get_host()]):
    #         next = '/'

    response = HttpResponseRedirect(next)
    if currency_code and Currency.active.filter(code=currency_code).exists():
        response.set_cookie(SESSION_KEY, currency_code)
        if hasattr(request, 'session'):
            request.session[SESSION_KEY] = currency_code
    return response


def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)
