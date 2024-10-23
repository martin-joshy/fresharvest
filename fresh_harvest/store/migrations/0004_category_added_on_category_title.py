# Generated by Django 4.2.8 on 2024-02-12 12:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_quantityvariant_product_quantity_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='added_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='category',
            name='title',
            field=models.CharField(db_index=True, default=None, max_length=350),
            preserve_default=False,
        ),
    ]
