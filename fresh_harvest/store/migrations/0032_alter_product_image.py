# Generated by Django 5.0.2 on 2024-10-12 04:06

import image_cropping.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=image_cropping.fields.ImageCropField(upload_to='images/'),
        ),
    ]
