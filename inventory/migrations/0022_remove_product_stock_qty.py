# Generated by Django 4.1.3 on 2022-12-19 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_remove_productattribute_sale_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock_qty',
        ),
    ]
