# Generated by Django 5.0.2 on 2024-03-25 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_remove_profile_wallet_wallettransaction_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WalletTransaction',
        ),
    ]