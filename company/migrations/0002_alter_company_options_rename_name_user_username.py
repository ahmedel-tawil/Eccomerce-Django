# Generated by Django 4.1.3 on 2022-11-30 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Company Profile'},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]