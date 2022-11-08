# Generated by Django 3.2.15 on 2022-11-05 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='floating_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
