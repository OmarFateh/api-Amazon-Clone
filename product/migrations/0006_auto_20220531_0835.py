# Generated by Django 2.2.19 on 2022-05-31 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20220530_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='brand.Brand'),
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
