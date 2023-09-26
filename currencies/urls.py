from django.urls import path
from currencies.views import set_currency, selectcurrency

urlpatterns = [
    path('setcurrency/', set_currency, name='currencies_set_currency'),

]
