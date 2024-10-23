# Generated by Django 5.0.2 on 2024-03-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
