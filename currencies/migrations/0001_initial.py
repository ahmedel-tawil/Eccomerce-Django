# Generated by Django 4.1.3 on 2022-12-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False, verbose_name='code')),
                ('name', models.CharField(db_index=True, max_length=55, verbose_name='name')),
                ('symbol', models.CharField(blank=True, db_index=True, max_length=4, verbose_name='symbol')),
                ('factor', models.DecimalField(decimal_places=10, default=1.0, help_text='Specifies the currency rate ratio to the base currency.', max_digits=30, verbose_name='factor')),
                ('is_active', models.BooleanField(default=True, help_text='The currency will be available.', verbose_name='active')),
                ('is_base', models.BooleanField(default=False, help_text='Make this the base currency against which rate factors are calculated.', verbose_name='base')),
                ('is_default', models.BooleanField(default=False, help_text='Make this the default user currency.', verbose_name='default')),
                ('info', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
                'ordering': ['name'],
            },
        ),
    ]
