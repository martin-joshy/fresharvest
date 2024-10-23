# Generated by Django 5.0.2 on 2024-03-15 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0022_rename_aprroved_seller_approved'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ReferralOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_redeemed', models.BooleanField(default=False)),
                ('referred_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to=settings.AUTH_USER_MODEL)),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referral_offers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]