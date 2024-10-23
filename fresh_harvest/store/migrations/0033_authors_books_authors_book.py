# Generated by Django 5.0.2 on 2024-10-21 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('published_on', models.DateField()),
                ('review', models.IntegerField(max_length=10)),
                ('author', models.ManyToManyField(to='store.authors')),
            ],
        ),
        migrations.AddField(
            model_name='authors',
            name='book',
            field=models.ManyToManyField(to='store.books'),
        ),
    ]