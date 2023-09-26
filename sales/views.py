import os
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.views import View

from shipping.models import ShoppingRate
from .tasks import send_oc_mail_task
from company.models import User, Company
from inventory.models import Product
from sales.forms import CheckoutForm, CouponForm, PaymentForm
from sales.models import OrderItem, Order, Address, Coupon, Payment, UserProfile, CustomerFavourite, \
    CustomerFavouriteItems
from sales.utils import is_valid_form, create_ref_code
import stripe
import pdfkit

wkhtml_to_pdf = os.path.join(
    settings.BASE_DIR, "wkhtmltopdf.exe")
stripe.api_key = settings.STRIPE_SECRET_KEY


def pdf_invoice(request, slug):
    options = {
        'page-size': 'A3',
        'page-height': "11in",
        'page-width': "8.5in",
        'margin-top': '0in',
        'margin-right': '1in',
        'margin-bottom': '0in',
        'margin-left': '1in',
        'encoding': "UTF-8",
        "enable-local-file-access": "",
        'no-outline': None
    }
    order = Order.objects.get(slug=slug)
    company = Company.objects.get(is_active=True)
    template_path = 'home/invoice_pdf.html'
    template = get_template(template_path)
    context = {
        'order': order,
        'company': company,
    }
    html = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = f'filename="order {order.slug}.pdf"'

    if response.status_code != 200:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
# def add_to_favourite(request, slug):
#     item = Product.objects.get(slug=slug)
#     items, created = CustomerFavouriteItems.objects.get_or_create(
#         user=request.user,
#         items=item
#     )
#     fav_qs = CustomerFavourite.objects.filter(user=request.user)
#     if fav_qs.exists():
#         fav_list = fav_qs[0]
#         if fav_list.items.filter(items__slug=item.slug).exists():
#             messages.info(request, "this item already in you favorite list")
#             return HttpResponse("Success!")
#         else:
#
#             items.save()
#             fav_list.items.add(items)
#             messages.info(request, f'The item {items.items.name} added to your favourite list.')
#             # return redirect("core:order-summary")
#             # return redirect("shopping")
#             return HttpResponse("Success!")
#     else:
#         added_at = timezone.now()
#         fav_list = CustomerFavourite.objects.create(
#             user=request.user, added_at=added_at)
#         items.save()
#         fav_list.items.add(items)
#         messages.info(request, "This item was added to your cart.")
#         return HttpResponse("Success!")
#
#     # if user_favourite

def add_to_favourite(request):
    if request.method == 'GET':
        product_slug = request.GET.get('product_slug')
        item = Product.objects.get(slug=product_slug)
        items, created = CustomerFavouriteItems.objects.get_or_create(
            user=request.user,
            items=item
        )
        fav_qs = CustomerFavourite.objects.filter(user=request.user)
        if fav_qs.exists():
            fav_list = fav_qs[0]
            if fav_list.items.filter(items__slug=item.slug).exists():
                messages.info(request, "this item already in you favorite list")
                return HttpResponse("Success!")
            else:

                items.save()
                fav_list.items.add(items)
                messages.info(request, f'The item {items.items.name} added to your favourite list.')
                # return redirect("core:order-summary")
                # return redirect("shopping")
                return HttpResponse("Success!")
        else:
            added_at = timezone.now()
            fav_list = CustomerFavourite.objects.create(
                user=request.user, added_at=added_at)
            items.save()
            fav_list.items.add(items)
            messages.info(request, "This item was added to your cart.")
            return HttpResponse("Success!")
    else:
        return HttpResponse("Request method is not a GET")

    # if user_favourite


# @login_required
# def add_to_cart(request, slug):
#     item = Product.objects.get(slug=slug)
#     attribute = item.productattribute_set.all().first()
#     order_item, created = OrderItem.objects.get_or_create(
#         product=item,
#         currency_id=1,
#         user=request.user,
#         ordered=False,
#         size=attribute,
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(product__slug=item.slug, size=attribute).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("shopping")
#         else:
#             order_item.price = attribute.price
#             order_item.size = attribute
#             order_item.save()
#             order.items.add(order_item)
#             messages.info(request, f'The item {order_item.product.name} added to your cart.')
#             # return redirect("core:order-summary")
#             return redirect("shopping")
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(
#             user=request.user, ordered_date=ordered_date)
#         order_item.price = attribute.price
#         order_item.size = attribute
#         order_item.save()
#         order.items.add(order_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("shopping")
#

## using HTMX Library
def add_to_cart(request, slug):
    item = Product.objects.get(slug=slug)
    attribute = item.productattribute_set.all().first()
    order_item, created = OrderItem.objects.get_or_create(
        product=item,
        currency_id=1,
        user=request.user,
        ordered=False,
        size=attribute,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug, size=attribute).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            html = "<html><body>Added.</body></html>"
            return HttpResponse(html)
        else:
            order_item.price = attribute.price
            order_item.size = attribute
            order_item.save()
            order.items.add(order_item)
            messages.info(request, f'The item {order_item.product.name} added to your cart.')
            # return redirect("core:order-summary")
            html = "<html><body>Added.</body></html>"
            return HttpResponse(html)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order_item.price = attribute.price
        order_item.size = attribute
        order_item.save()
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        html = "<html><body>Added.</body></html>"
        return HttpResponse(html)


@login_required
def add_to_cart_new(request, slug):
    name = request.GET.get("name-product")
    qty = request.GET.get("qty-product")
    if not qty:
        qty = 1
    size = request.GET.get("size-product")
    item = Product.objects.get(slug=slug)
    attribute = item.productattribute_set.get(size_id=size)
    order_item, created = OrderItem.objects.get_or_create(
        product=item,
        currency_id=1,
        user=request.user,
        ordered=False,
        size=attribute,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug, size=attribute).exists():
            order_item.quantity = qty
            order_item.save()
            messages.success(request,
                             f"The item {order_item.product.name} quantity was updated. Your Cart contains {order_item.quantity} of {order_item.product.name} ")
            return redirect("shopping")
        else:
            order_item.quantity = qty
            order_item.price = attribute.price
            order_item.size = attribute
            order_item.save()
            order.items.add(order_item)
            messages.success(request, f'The item {order_item.product.name} added to your cart.')
            return redirect("shopping")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order_item.quantity = qty
        order_item.price = attribute.price
        order_item.size = attribute
        order_item.save()
        order.items.add(order_item)
        messages.success(request, f'The item {order_item.product.name} added to your cart.')
        return redirect("shopping")


@login_required
def increase_cart_item_value(request, id):
    item = get_object_or_404(OrderItem, id=id)
    item.quantity += 1
    item.save()
    messages.success(request, f'your cart contains now  {item.quantity} of {item.product.name} ')
    return redirect("order-summary")


@login_required
def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug)
    count = product.productattribute_set.count()
    if request.method == 'POST':
        messages.info(request, 'Fetching data')
        name = request.POST.get("product-name")
        qty = request.POST.get("product-quantity")
        if not qty:
            qty = 1
        size = request.POST.get("product-size")
        messages.info(request, f'{name} -  {qty} - {size}')
        print(name, qty)
        if product.productattribute_set.filter(size_id=size).exists():
            attribute = product.productattribute_set.get(size_id=size)
        else:
            attribute = product.productattribute_set.all().first()
        order_item, created = OrderItem.objects.get_or_create(
            product=product,
            user=request.user,
            currency_id=1,
            ordered=False,
            size=attribute,
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(product__slug=product.slug, size=attribute).exists():
                order_item.quantity = qty
                order_item.price = attribute.price
                order_item.size = attribute
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                # return redirect("core:order-summary")
                return redirect("order-summary")
            else:
                # order.items.add(order_item)
                order_item.quantity = qty
                order_item.price = attribute.price
                order_item.size = attribute
                order_item.save()
                order.items.add(order_item)
                messages.info(request, f'The item {order_item.product.name} added to your cart.')
                # return redirect("core:order-summary")
                return redirect("order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order_item.quantity = qty
            order_item.price = attribute.price
            order_item.size = attribute
            order_item.save()
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")

    context = {
        'product': product
    }
    return render(request, 'home/shop-single.html', context)


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(OrderItem, id=id)
    item.delete()
    messages.error(request, f'the {item.product.name} deleted from your cart ')
    return redirect("order-summary")


@login_required
def remove_from_favourite(request, id):
    item = get_object_or_404(CustomerFavouriteItems, id=id)
    item.delete()
    messages.warning(request, f'The item {item.items.name}  removed from your favourite list')
    return redirect("shopping")


@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(OrderItem, id=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        messages.warning(request, f'your cart contains now  {item.quantity} of {item.product.name} ')
    else:
        item.delete()
        messages.error(request, f'the {item.product.name} deleted from your cart ')

    return redirect("order-summary")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'home/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("shopping")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs.last()})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs.last()})
            return render(self.request, "home/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs.last()
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                        return redirect('checkout')

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs.last()
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")
                        return redirect('checkout')

                # payment_option = form.cleaned_data.get('payment_option')
                return redirect('shipping-method')
                # payment_option = 'S'
                # if payment_option == 'S':
                #     return redirect('shipping-method')
                # elif payment_option == 'P':
                #     return redirect('payment', payment_option='paypal')
                # else:
                #     messages.warning(
                #         self.request, "Invalid payment option selected")
                #     return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")


class ShippingView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            if order.shipping_address:
                shipping_address_qs = order.shipping_address
                country = shipping_address_qs.country
                available_shipping_method = ShoppingRate.objects.filter(zone__country__contains=country).values(
                    'id', 'zone__country', 'rate_name', 'price', 'number_of_days', 'company__name')
                context.update(
                    {
                        'country': country,
                        'shipping_address_qs': shipping_address_qs,
                        'available_shipping_method': available_shipping_method,
                    })
            else:
                messages.warning(
                    self.request, "Please Add shipping Address Details")
                return redirect('shipping-method')
            if order.billing_address:
                billing_address_qs = order.billing_address
                context.update(
                    {'billing_address_qs': billing_address_qs})
            else:
                messages.warning(
                    self.request, "Please Add Billing Address Details")
                return redirect('shipping-method')
            return render(self.request, "home/shippment_method.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def apply_shipping(request, slug):
    order = Order.objects.get(slug=slug)
    if request.method == 'POST':
        # messages.info(request, 'Fetching data')
        ship_method = request.POST.get("ship-method")
        if ship_method:
            # fetch the Shipping Method
            order.shipping_method = ShoppingRate.objects.get(id=ship_method)
            order.save()
            messages.success(request, f'Successfully Added Shipping Method to your order')
            messages.success(request, f'Your order will be shipped by {order.shipping_method.company.name}')
            return redirect("payment")
        else:
            messages.warning(request, f'Please select a valid Shipping Method..')
            return redirect("shipping-method")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "home/payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')
            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id,
                    )
                    customer.create_source(
                        id=str(userprofile.stripe_customer_id),
                        source=token,
                    )

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                        name=self.request.user.username,
                    )
                    customer.create_source(
                        id=customer['id'],
                        source=token,
                    )
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()
            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="aed",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="aed",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()
                messages.success(self.request, "Your order was successful!")
                send_oc_mail_task(email=userprofile.user.email, order=order)
                ## Send Email here
                return redirect("shopping")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")


def approve_order(request, slug):
    order = Order.objects.get(slug=slug)
    if order.order_transit == True:
        messages.warning(request, "Order already sent for shipping ")
        return HttpResponseRedirect(reverse('admin:sales_order_changelist'))
    else:
        order.order_transit = True
        order.save()
    return HttpResponseRedirect(reverse('admin:sales_order_changelist'))

# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)
