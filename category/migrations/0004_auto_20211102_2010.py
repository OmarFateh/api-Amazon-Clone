# Generated by Django 2.2.19 on 2021-11-02 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_auto_20210822_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'parent')},
        ),
    ]
