# Generated by Django 5.0.2 on 2024-02-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_rename_aprroved_seller_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='approved',
        ),
        migrations.AddField(
            model_name='seller',
            name='aprroved',
            field=models.BooleanField(default=False),
        ),
    ]
