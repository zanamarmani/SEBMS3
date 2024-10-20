# Generated by Django 5.1 on 2024-10-10 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meterreader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meter',
            name='meter_type',
            field=models.CharField(choices=[('single', 'Single Phase'), ('double', 'Double Phase'), ('three', 'Three Phase')], max_length=10, null=True),
        ),
    ]
