# Generated by Django 4.1.3 on 2022-12-06 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_sizeunit_alter_size_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.sizeunit'),
        ),
    ]
