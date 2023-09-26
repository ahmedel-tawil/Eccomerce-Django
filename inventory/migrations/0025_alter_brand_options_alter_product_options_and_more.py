# Generated by Django 4.1.3 on 2022-12-21 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_product_is_feature'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Brand', 'verbose_name_plural': '2 - Brands List'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_at',), 'verbose_name': 'Product', 'verbose_name_plural': '3 - Products List'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'verbose_name_plural': '4 - Product Attributes'},
        ),
    ]
