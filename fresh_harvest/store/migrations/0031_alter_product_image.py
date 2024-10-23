# Generated by Django 5.0.2 on 2024-03-29 14:52

import image_cropping.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_product_image_ratio_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=image_cropping.fields.ImageCropField(default='dummy', upload_to='images/'),
        ),
    ]
