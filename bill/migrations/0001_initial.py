# Generated by Django 5.1 on 2024-10-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billmonth', models.DateField(null=True)),
                ('duedate', models.DateField(blank=True, null=True)),
                ('detectionunit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('averageunit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('units', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('unitsconsumed', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('payableamount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('payable_after_due_date', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False, null=True)),
            ],
        ),
    ]
