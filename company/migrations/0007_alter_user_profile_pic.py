# Generated by Django 4.1.3 on 2022-12-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_rename_ie_customer_user_is_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='static/images/user-avatar.png', upload_to='images/users-profile-pics'),
        ),
    ]