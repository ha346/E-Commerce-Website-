# Generated by Django 4.0.6 on 2023-01-13 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orderupdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderupdate',
            old_name='update_desc',
            new_name='order_desc',
        ),
    ]
