import urllib
from urllib.parse import urlparse

from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.files.base import ContentFile, File
from django.core.files.temp import NamedTemporaryFile
from django.forms import BaseInlineFormSet
from django.utils.html import format_html

from django.urls import reverse
from django.utils.http import urlencode
from import_export import resources, fields
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export.widgets import ForeignKeyWidget

from .models import *
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

import os
import requests
from django.core.files.base import ContentFile


# Register your models here.

def save_image_from_row(instance, row):
    if row['main_image']:
        if row['main_image'] == instance.main_image:
            image_content = ContentFile(requests.get(row['main_image']).content)
            url_image = urlparse(row['main_image'])
            instance.main_image.save(os.path.basename(url_image.path), image_content)
            instance.save()


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that at least one service has been entered."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                   for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('please add size and price data for your product')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name',)


admin.site.register(Brand, BrandAdmin)


class CategoryAdmin(MPTTModelAdmin):
    mptt_ident_field = "name"
    list_display = (
        'name', 'code', 'related_products_count', 'related_products_cumulative_count')

    # list_display_links = ('indented_title',)
    # list_editable = ('code',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(Category, CategoryAdmin)

admin.site.register(Specification)

admin.site.register(SizeUnit)
admin.site.register(Size)


# Product Attribute

class ProductAttributeResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'code'))
    size = fields.Field(
        column_name='size',
        attribute='size',
        widget=ForeignKeyWidget(Size, 'title'))

    item_cost = fields.Field(attribute='price', column_name='item_cost')
    regular_price = fields.Field(attribute='product_price', column_name='regular_price')
    discount_price = fields.Field(attribute='discount_price', column_name='discount_price')

    class Meta:
        model = ProductAttribute
        fields = (
            'id', 'product', 'size', 'sku', 'qty', 'item_cost', 'regular_price', 'discount_price', 'image')
        import_id_fields = ('id',)

    def __init__(self):
        super(ProductAttributeResource, self).__init__()
        # Introduce a class variable to pass dry_run into methods that do not get it
        self.in_dry_run = False

    # def skip_row(self, instance, original):
    #     if original.id:
    #         return False
    #     return super(ProductAttributeResource, self).skip_row(self, instance, original)

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if original.id:
            return False
        return super(ProductAttributeResource, self).skip_row(instance, original, row,
                                                              import_validation_errors=import_validation_errors)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Set helper class method to dry_run value
        self.in_dry_run = dry_run


class ProductAttributeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'product', 'qty', 'sku', 'price', 'product_price', 'discount_price', 'size',
                    ProductAttribute.get_currency)

    list_display_links = ('id', 'image_tag', 'product',)

    list_filter = ('product__name', 'product__category')
    search_fields = 'sku',
    search_help_text = 'search by SKU value'
    # list_editable = ('sku', 'price', 'product_price', 'discount_price',)
    list_per_page = 30
    resource_classes = [ProductAttributeResource]


admin.site.register(ProductAttribute, ProductAttributeAdmin)


class ProductImagesInline(admin.TabularInline):
    model = ProductImages


class ProductSpecInline(admin.TabularInline):
    model = ProductSpecification


class ProductAttributeAdminInline(admin.TabularInline):
    model = ProductAttribute
    formset = AtLeastOneRequiredInlineFormSet


class ProductResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name='name')

    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'code'))

    currency = fields.Field(
        column_name='currency',
        attribute='currency',
        widget=ForeignKeyWidget(Currency, 'symbol'))

    # created_by = models.Field   column_name='currency',
    #     attribute='currency',
    #     widget=ForeignKeyWidget(Currency, 'symbol')

    class Meta:
        model = Product
        fields = (
            'id', 'code', 'name', 'category', 'currency', 'main_image', 'description_l', 'description_s', 'created_by')
        import_id_fields = ('id',)

    def __init__(self):
        super(ProductResource, self).__init__()
        # Introduce a class variable to pass dry_run into methods that do not get it
        self.in_dry_run = False

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Set helper class method to dry_run value
        self.in_dry_run = dry_run
    
    def before_import_row(self, row, row_number=None, **kwargs):
        row['created_by'] = kwargs['user'].id


class ProductAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('code', 'name', 'slug', 'category', 'view_attributes', Product.get_created_by)
    inlines = [ProductImagesInline, ProductAttributeAdminInline, ProductSpecInline]
    fieldsets = (
        ('Product identification', {
            'fields': ('name', 'code', 'main_image', 'description_s', 'description_l')
        }), ('Category and Brand', {
            'fields': ('category', 'brand')
        }),
    )
    resource_classes = [ProductResource]
    list_per_page = 15

    def view_attributes(self, obj):
        count = obj.productattribute_set.count()
        url = (
                reverse("admin:inventory_productattribute_changelist")
                + "?"
                + urlencode({"product__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} # Attributes</a>', url, count)

    view_attributes.short_description = "# Attributes"

    # list_editable = ('name',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, change, form)


admin.site.register(Product, ProductAdmin)
