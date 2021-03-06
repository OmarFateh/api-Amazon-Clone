# Generated by Django 2.2.19 on 2021-12-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20211105_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='max_price',
        ),
        migrations.AlterField(
            model_name='product',
            name='total_in_stock',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='max_price',
            field=models.DecimalField(decimal_places=2, default=500, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='total_in_stock',
            field=models.PositiveIntegerField(),
        ),
    ]
