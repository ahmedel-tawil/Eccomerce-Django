# Generated by Django 4.1.3 on 2022-12-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_user_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name='Company'),
        ),
        migrations.AddField(
            model_name='company',
            name='is_shipping',
            field=models.BooleanField(default=False, help_text='Designate the Company to be Supplier', verbose_name='Shipping Company'),
        ),
        migrations.AddField(
            model_name='company',
            name='is_supplier',
            field=models.BooleanField(default=False, help_text='Designate the Company to be Supplier', verbose_name='Supplier Company'),
        ),
    ]
