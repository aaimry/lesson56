# Generated by Django 4.0.1 on 2022-02-07 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_products_options_alter_products_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Колличество'),
        ),
    ]
