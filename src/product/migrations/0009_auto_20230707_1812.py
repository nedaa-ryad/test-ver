# Generated by Django 3.2.17 on 2023-07-07 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20230707_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email_verification_token',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_email_verified',
        ),
    ]
