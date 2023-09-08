# Generated by Django 3.2.17 on 2023-06-06 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_prd_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='PRD_Category',
            field=models.CharField(choices=[('BE', 'Bed'), ('SO', 'Sofa'), ('CA', 'Chair'), ('LI', 'Lighting'), ('TA', 'Table'), ('DT', 'Dining_Table')], max_length=2, verbose_name='Category'),
        ),
    ]
