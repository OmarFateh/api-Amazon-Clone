# Generated by Django 2.2.19 on 2021-08-22 12:32

import category.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20210813_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=category.fields.TitleCharField(max_length=64),
        ),
    ]
