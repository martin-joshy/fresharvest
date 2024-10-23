# Generated by Django 5.0.2 on 2024-03-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled'), ('payment_pending', 'payment_pending')], default='Pending', max_length=20),
        ),
    ]
