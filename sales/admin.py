from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from sales.models import Order, OrderItem, Payment, Coupon, Refund, Address, UserProfile


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def send_order_for_shipping(modeladmin, request, queryset):
    queryset.update(order_transit=True)


send_order_for_shipping.short_description = 'Send Orders for Shipping'


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = [Order.get_created_by,
                    Order.get_time_display,
                    Order.get_date_display,
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'order_transit',
                    'approve',
                    # 'shipping_address',
                    # 'billing_address',
                    # 'payment',
                    # 'coupon'
                    ]
    list_display_links = [
        Order.get_created_by,
        # 'shipping_address',
        # 'billing_address',
        # 'payment',
        # 'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    list_per_page = 15
    date_hierarchy = ('start_date')

    def approve(self, obj):
        view_name = "approve_order"
        link = reverse(view_name, args=[obj.slug])
        html = '<input class="btn btn-primary" type="button" onclick="location.href=\'{}\'" value="ship order" />'.format(
            link)
        return format_html(html)

    actions = [send_order_for_shipping, make_refund_accepted, ]


admin.site.register(Order, OrderAdmin)


class ToPackOrder(Order):
    class Meta:
        proxy = True
        verbose_name_plural = 'orders To Pack'


class ToPackAdmin(OrderAdmin):

    def get_queryset(self, request):
        return self.model.objects.filter(order_transit=True)


admin.site.register(ToPackOrder, ToPackAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(OrderItem)

admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')


admin.site.register(Payment, PaymentAdmin)
#
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pubdate','user')
#
# class MyPost(Post):
#     class Meta:
#         proxy = True
#
# class MyPostAdmin(PostAdmin):
#     def get_queryset(self, request):
#         return self.model.objects.filter(user = request.user)
#
#
# admin.site.register(Post, PostAdmin)
# admin.site.register(MyPost, MyPostAdmin)
