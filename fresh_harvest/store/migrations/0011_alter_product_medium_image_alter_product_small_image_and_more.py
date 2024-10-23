# Generated by Django 5.0.2 on 2024-02-21 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_product_medium_image_product_small_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='medium_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/medium/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='small_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/small/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001BEA60BA980>', max_length=200),
        ),
    ]
