# Generated by Django 5.1 on 2024-10-29 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='arrears',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
