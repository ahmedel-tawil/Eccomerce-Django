from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now

from currencies.models import Currency
from inventory.utils import unique_slug_generator
from .manager import UserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session


# Create your models here.
class Company(models.Model):
    name = models.CharField(_('company name'), max_length=300)
    website = models.URLField(_('Company Website'), blank=True, null=True)
    email = models.EmailField(_('Company Email'), blank=True, null=True)
    logo = models.ImageField(_('Company Logo'), upload_to='images/company-logos', )
    business_type = models.CharField(_('Business Type'), max_length=100)  # add choicess to this
    description = models.TextField(_('Description'), max_length=500)
    facebook = models.URLField(_('Company Facebook'), blank=True, null=True)
    twitter = models.URLField(_('Company Twitter'), blank=True, null=True)
    instagram = models.URLField(_('Company Instagram'), blank=True, null=True)
    linkedin = models.URLField(_('Company LinkedIn'), blank=True, null=True)
    phone_number = PhoneNumberField(_('Phone Number'), blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(_('Active'), help_text='Designate the Company to be an Active Company',
                                    default=True)
    is_main = models.BooleanField(_('Company'), help_text='Designate the Company to be the Main Company', default=False)
    is_supplier = models.BooleanField(_('Supplier Company'), default=False,
                                      help_text='Designate the Company to be Supplier')
    is_shipping = models.BooleanField(_('Shipping Company'), default=False,
                                      help_text='Designate the Company to be Shipping')

    # to add data like phone, location , etc..
    # limit this class for one record
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Company Profile'

    def __str__(self):
        return f'{self.name}'

    def clean(self):
        if self.is_main:
            main = Company.objects.filter(is_main=True)
            if self.pk:
                main = main.exclude(pk=self.pk)
            if main.exists():
                raise ValidationError(
                    f"A company is already registered as a main, please un check the company check box")


class Departments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    name = models.CharField(_('Department Name'), max_length=200)

    def __str__(self):
        return f'{self.name}'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(_('Account Owner Name'), max_length=100)
    phone_number = PhoneNumberField(_('Phone Number'))
    phone_number2 = PhoneNumberField(_('Mobile Number'), blank=True, null=True)
    profile_pic = models.ImageField(upload_to='images/users-profile-pics', default='static/images/user-avatar.png')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, blank=True, null=True)

    otp = models.SmallIntegerField(_('OTP'), help_text='one time password', null=True, blank=True)
    token = models.CharField(_('Token'), unique=True, help_text='Token For Authentication', null=True, blank=True,
                             editable=False, max_length=100)
    ip_address = models.GenericIPAddressField(_('Ip Address'), blank=True, null=True)

    is_verified = models.BooleanField(_('Verified'), default=False,
                                      help_text='is this user is Verified, unverified users cannot Login')

    is_founder = models.BooleanField(_('Founder'), default=False,
                                     help_text='Designate the user to be Founder')
    is_ceo = models.BooleanField(_('CEO'), default=False,
                                 help_text='Designate the user to be CEO')

    is_admin = models.BooleanField(_('Admin'), default=False,
                                   help_text='Designate the user to be Admin')
    is_manger = models.BooleanField(_('Manager'), default=False,
                                    help_text='Designate the user to be Manager')

    is_headoffice = models.BooleanField(_('Head Office'), default=False,
                                        help_text='Designate the user to be office head')

    is_hr = models.BooleanField(_('Human Resources'), default=False,
                                help_text='Designate the user to be HR')

    is_accountant = models.BooleanField(_('Accountant'), default=False,
                                        help_text='Designate the user to be Accountant')

    is_employee = models.BooleanField(_('Employee'), default=False,
                                      help_text='Designate the user to be Employee')
    is_customer = models.BooleanField(_('Customer'), default=False,
                                      help_text='Designate the user to be Customer')

    is_supplier = models.BooleanField(_('Supplier'), default=False,
                                      help_text='Designate the user to be Supplier')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)

    otp_creation_datetime = models.DateTimeField(_('OTP created Time'), default=now, editable=False)
    password_change_datetime = models.DateTimeField(_('Password Change Time'), blank=True, null=True)
    login_datetime = models.DateTimeField(_('Log in Time'), blank=True, null=True)
    logout_datetime = models.DateTimeField(_('Log out Time'), blank=True, null=True)
    last_activity = models.DateTimeField(_('Last activity Time'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    session = models.OneToOneField(Session, on_delete=models.CASCADE, blank=True, null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    objects = UserManager()

    def get_profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return 'static/images/user-avatar.png'

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


@receiver(pre_save, sender=User)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Currency(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    symbol = models.CharField(max_length=5)

    factor = models.FloatField(default=1, help_text=_('Specifies the currency rate ratio to the base currency.'))

    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('The currency will be available.'))
    is_base = models.BooleanField(_('base'), default=False,
                                  help_text=_('Make this the base currency against which rate factors are calculated.'))
    is_default = models.BooleanField(_('default'), default=False,
                                     help_text=_('Make this the default user currency.'))

    class Meta:
        ordering = ['name']
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return f'{self.name}  + {self.country}'

    def save(self, **kwargs):
        # Make sure the base and default currencies are unique
        if self.is_base is True:
            self.__class__._default_manager.filter(is_base=True).update(is_base=False)

        if self.is_default is True:
            self.__class__._default_manager.filter(is_default=True).update(is_default=False)

        # Make sure default / base currency is active
        if self.is_default or self.is_base:
            self.is_active = True

        super(Currency, self).save(**kwargs)
