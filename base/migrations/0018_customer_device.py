# Generated by Django 4.1.4 on 2023-03-09 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_rename_items_order_configurations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='device',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
