# Generated by Django 5.0.2 on 2024-03-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20),
        ),
    ]
