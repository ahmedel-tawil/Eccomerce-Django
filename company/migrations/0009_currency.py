# Generated by Django 4.1.3 on 2022-12-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_company_address_company_facebook_company_instagram_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=5)),
            ],
        ),
    ]
