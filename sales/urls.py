from django.urls import path
from .views import *

# app_name = ['online-sales']
urlpatterns = [
    # original
    # path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    # HTMX
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add_to_cart_new/<slug>/', add_to_cart_new, name='add_to_cart_new'),

    path('apply_shipping/<slug>/', apply_shipping, name='apply_shipping'),

    # path('add_to_favourite/<slug>/', add_to_favourite, name='add-to-favourite'),
    path('add_to_favourite/', add_to_favourite, name='add-to-favourite'),

    path('approve_order/<slug>/', approve_order, name='approve_order'),
    path('pdf_invoice/<slug>/', pdf_invoice, name='pdf-invoice'),
    path('update-to-cart/<id>/', increase_cart_item_value, name='update_to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('details/<str:slug>/', product_detail_view, name='product-det'),
    path('remove-from-cart/<id>/', remove_from_cart, name='remove-from-cart'),
    path('remove_from_favourite/<id>/', remove_from_favourite, name='remove_from_favourite'),

    path('remove-item-from-cart/<id>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('shipping/', ShippingView.as_view(), name='shipping-method'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),

    path('payment/', PaymentView.as_view(), name='payment'),

    # path('cart', cart_list, name='cart'),

]
