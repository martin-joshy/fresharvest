# Generated by Django 5.0.2 on 2024-03-21 13:06

import slick_reporting.generator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReportGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            bases=(models.Model, slick_reporting.generator.ReportGenerator),
        ),
    ]
