# Generated by Django 4.1.3 on 2022-12-09 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_customerfavourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_transit',
            field=models.BooleanField(default=False),
        ),
    ]