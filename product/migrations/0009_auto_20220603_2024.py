# Generated by Django 2.2.19 on 2022-06-03 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_product_brand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariantimage',
            old_name='is_thumbnail',
            new_name='is_default',
        ),
    ]
