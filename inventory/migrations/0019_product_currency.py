# Generated by Django 4.1.3 on 2022-12-08 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_currency_country'),
        ('inventory', '0018_alter_productattribute_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.currency'),
            preserve_default=False,
        ),
    ]
