# Generated by Django 4.1.3 on 2022-12-05 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_category_description_l_category_description_s_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/product-images'),
        ),
    ]
