# Generated by Django 3.2.4 on 2022-02-21 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_aboutme_shopuserprofile_about_me'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShopUserProfile',
        ),
    ]
