# Generated by Django 3.2.17 on 2023-06-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_prd_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='PRD_Image',
            field=models.ImageField(blank=True, null=True, upload_to='Product', verbose_name='Product Image'),
        ),
    ]
