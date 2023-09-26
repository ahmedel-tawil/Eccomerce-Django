# Generated by Django 4.1.3 on 2022-12-08 07:55

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='country',
            field=django_countries.fields.CountryField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
