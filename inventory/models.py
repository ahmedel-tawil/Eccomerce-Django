from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from mptt.models import MPTTModel
from treewidget.fields import TreeForeignKey
from django.utils.translation import gettext_lazy as _

from company.models import User, Currency

from inventory.utils import unique_slug_generator


# Create your models here.

class ProductManager(models.Manager):
    def get_query_set(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


# Inventory Category
class Category(MPTTModel):
    name = models.CharField(_('Category Name'), max_length=50, unique=True)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)
    description_l = models.TextField(_('Category Description'), help_text='Category long description', max_length=500,
                                     blank=True, null=True)
    description_s = models.CharField(_('Category Description'), help_text='Category short description', max_length=200,
                                     blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    code = models.CharField(_('Category Code'), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = _('Category Tree')
        verbose_name_plural = 'Category Tree'

    def __str__(self):
        return f'{self.name}'

    def get_total_sales(self):
        total_sales = Category.objects.filter(id=self.id).values('product__orderitem__price').aggregate(
            Sum('product__orderitem__price'))['product__orderitem__price__sum']
        return total_sales


class Brand(models.Model):
    name = models.CharField(_('Brand Name'), max_length=100)
    image = models.ImageField(_('Brand Image'), upload_to='images/brand-images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Brands List'
        verbose_name = 'Brand'

    def __str__(self):
        return f'{self.name}'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:
            return ''


class SizeUnit(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Perfume SizeUnit'

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=100)
    unit = models.ForeignKey(SizeUnit, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(_('Product name'), max_length=100)
    code = models.CharField(_('Product Code'), max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200)
    parcode = models.ImageField(upload_to='images/product-parcode', blank=True, null=True)
    qrcode = models.ImageField(upload_to='images/product-parcode', blank=True, null=True)
    main_image = models.ImageField(upload_to='images/product-images', blank=True, null=True)
    description_l = models.TextField(_('Product Description'), help_text='Product long description', max_length=500,
                                     blank=True, null=True)
    description_s = models.CharField(_('Product Description'), help_text='Product short description', max_length=200,
                                     blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products List'
        ordering = '-created_at',

    def __str__(self):
        return f'{self.name}'

    def get_created_by(self):
        return self.created_by.name

    get_created_by.short_description = 'Added By'

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_absolute_url(self):
        return reverse('item-details', args=[str(self.slug)])


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product-images', blank=True, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    is_feature = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'


# Product Attribute
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField(_('Item Cost'), default=0, help_text='Item Cost')
    qty = models.FloatField(default=0)
    sku = models.CharField(_('SKU'), help_text='stock keeping unit', max_length=50, blank=True, null=True)
    product_price = models.FloatField(_('Regular Price'), default=0)
    discount_price = models.FloatField(_('discount price'), blank=True, null=True)
    image = models.ImageField(upload_to="product_imgs/", null=True)

    class Meta:
        verbose_name_plural = 'Product Attributes'

    def __str__(self):
        return self.product.name

    def get_currency(self):
        return self.product.currency.symbol

    get_currency.short_description = 'Currency'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:
            return ''


class Specification(models.Model):
    name = models.CharField(max_length=100, )

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value
