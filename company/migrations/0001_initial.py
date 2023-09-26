# Generated by Django 4.1.3 on 2022-11-30 05:37

import company.manager
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='company name')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Company Website')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Company Email')),
                ('logo', models.ImageField(upload_to='images/company-logos', verbose_name='Company Logo')),
                ('business_type', models.CharField(max_length=100, verbose_name='Business Type')),
                ('description', models.TextField(max_length=500, verbose_name='Description')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Department Name')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Account Owner Name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone Number')),
                ('phone_number2', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Mobile Number')),
                ('profile_pic', models.ImageField(upload_to='images/users-profile-pics')),
                ('otp', models.SmallIntegerField(blank=True, help_text='one time password', null=True, verbose_name='OTP')),
                ('token', models.CharField(blank=True, editable=False, help_text='Token For Authentication', max_length=100, null=True, unique=True, verbose_name='Token')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip Address')),
                ('is_verified', models.BooleanField(default=False, help_text='is this user is Verified, unverified users cannot Login', verbose_name='Verified')),
                ('is_founder', models.BooleanField(default=False, help_text='Designate the user to be Founder', verbose_name='Founder')),
                ('is_ceo', models.BooleanField(default=False, help_text='Designate the user to be CEO', verbose_name='CEO')),
                ('is_admin', models.BooleanField(default=False, help_text='Designate the user to be Admin', verbose_name='Admin')),
                ('is_manger', models.BooleanField(default=False, help_text='Designate the user to be Manager', verbose_name='Manager')),
                ('is_headoffice', models.BooleanField(default=False, help_text='Designate the user to be office head', verbose_name='Head Office')),
                ('is_hr', models.BooleanField(default=False, help_text='Designate the user to be HR', verbose_name='Human Resources')),
                ('is_accountant', models.BooleanField(default=False, help_text='Designate the user to be Accountant', verbose_name='Accountant')),
                ('ie_employee', models.BooleanField(default=False, help_text='Designate the user to be Employee', verbose_name='Employee')),
                ('ie_customer', models.BooleanField(default=False, help_text='Designate the user to be Customer', verbose_name='Customer')),
                ('ie_supplier', models.BooleanField(default=False, help_text='Designate the user to be Supplier', verbose_name='Supplier')),
                ('otp_creation_datetime', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='OTP created Time')),
                ('password_change_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Password Change Time')),
                ('login_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Log in Time')),
                ('logout_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Log out Time')),
                ('last_activity', models.DateTimeField(blank=True, null=True, verbose_name='Last activity Time')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='company.company')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='company.departments')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('session', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', company.manager.UserManager()),
            ],
        ),
    ]
