# Generated by Django 4.1.3 on 2022-12-27 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_currency_is_basic_currency_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'ordering': ['name'], 'verbose_name': 'currency', 'verbose_name_plural': 'currencies'},
        ),
        migrations.RemoveField(
            model_name='currency',
            name='is_basic',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='rate',
        ),
        migrations.AddField(
            model_name='currency',
            name='factor',
            field=models.FloatField(default=1, help_text='Specifies the currency rate ratio to the base currency.'),
        ),
        migrations.AddField(
            model_name='currency',
            name='is_active',
            field=models.BooleanField(default=True, help_text='The currency will be available.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='currency',
            name='is_base',
            field=models.BooleanField(default=False, help_text='Make this the base currency against which rate factors are calculated.', verbose_name='base'),
        ),
        migrations.AddField(
            model_name='currency',
            name='is_default',
            field=models.BooleanField(default=False, help_text='Make this the default user currency.', verbose_name='default'),
        ),
    ]
