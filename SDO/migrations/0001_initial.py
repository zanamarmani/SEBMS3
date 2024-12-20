# Generated by Django 5.1 on 2024-10-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sdo_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('office_location', models.CharField(max_length=255, null=True)),
                ('joining_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tariff_type', models.CharField(choices=[('domestic', 'Domestic'), ('commercial', 'Commercial'), ('industrial', 'Industrial')], max_length=10)),
                ('price_100', models.DecimalField(decimal_places=2, default=3, max_digits=10)),
                ('price_200', models.DecimalField(decimal_places=2, default=4, max_digits=10)),
                ('price_300', models.DecimalField(decimal_places=2, default=5, max_digits=10)),
                ('price_above', models.DecimalField(decimal_places=2, default=6, max_digits=10)),
            ],
            options={
                'verbose_name_plural': 'Tariffs',
            },
        ),
    ]
