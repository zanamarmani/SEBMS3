# Generated by Django 5.1 on 2024-10-10 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0004_consumer_meter_type_alter_consumer_consumer_division'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumer',
            name='meter_type',
        ),
    ]
