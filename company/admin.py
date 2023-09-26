from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
# from django.contrib.gis.utils import GeoIP
from django.utils.safestring import mark_safe

from .forms import CompanyModelForm
from .models import User, Company, Departments, Currency


# Register your models here.
# class CurrencyAdmin(admin.ModelAdmin):
#     list_display = ("name", 'country', "is_active", "is_base", "is_default", "symbol", "factor")
#     list_filter = ("is_active",)
#     search_fields = ("name", "code")
#     form = CurrencyModelForm
#
#
# admin.site.register(Currency, CurrencyAdmin)


class DptAdminInlines(admin.TabularInline):
    model = Departments


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_profile_logo', 'name', 'website', 'email', 'business_type')
    inlines = [DptAdminInlines, ]

    form = CompanyModelForm

    def company_profile_logo(self, obj):
        return format_html(f'<img src="{obj.logo.url}" width="40" height="40"/>')

    company_profile_logo.short_description = 'Logo'


admin.site.register(Company, CompanyAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_profile_pic', 'name', 'email', 'phone_number',
                    'is_superuser', 'is_staff', 'change', 'history')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('token',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'email', 'phone_number', 'company', 'department', 'currency')
        }),
        ('Profile Picture', {
            'fields': ('profile_pic',)
        }),
        ('Timestamps⏳', {
            # 'classes': ('collapse',),
            'fields': (
                'date_joined', 'password_change_datetime', 'login_datetime', 'logout_datetime', 'last_activity'),
            'description': 'Timestamps fields are automatically updated by the system.'
        }),
        ('Permissions🔐', {
            #  'classes': ('collapse',),
            'fields': (
                ('is_verified', 'is_superuser', 'is_active',
                 'is_staff', 'is_founder', 'is_ceo', 'is_manger',
                 'is_employee', 'is_customer', 'is_supplier',
                 'is_headoffice', 'is_hr', 'is_accountant'),
            ),
            'description': 'Note: If you want to change the permissions of a user, you need to contact in our headquarters.'
        }),
        ('Session🛢', {
            # 'classes': ('collapse',),
            'fields': ('session',)
        }),
        ('Secret🔐', {
            # 'classes': ('collapse',),
            'fields': ('token',)
        }),
        ('Groups🏷', {
            # 'classes': ('collapse',),
            'fields': ('groups',)
        }),
    )

    def user_profile_pic(self, obj):
        try:
            return format_html(f'<img src="{obj.profile_pic.url}" width="40" height="40"/>')
        except:
            return format_html(f'<img src="static/images/user-avatar.png" width="40" height="40"/>')

    user_profile_pic.short_description = 'Profile'

    def change(self, obj):
        view_name = "admin:{}_{}_change".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.pk])
        html = '<input class="btn btn-primary" type="button" onclick="location.href=\'{}\'" value="Change" />'.format(
            link)
        return format_html(html)

    def history(self, obj):
        view_name = "admin:{}_{}_history".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.pk])
        html = '<input class="btn btn-primary" type="button" onclick="location.href=\'{}\'" value="History" />'.format(
            link)
        return format_html(html)


admin.site.unregister(Group)
