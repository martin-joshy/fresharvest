# Generated by Django 5.0.2 on 2024-03-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_address_post_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='post_code',
            field=models.PositiveIntegerField(max_length=6),
        ),
    ]