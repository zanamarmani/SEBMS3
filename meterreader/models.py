from django.db import models

from consumer.models import Consumer

class Meter(models.Model):
    METER_TYPE_CHOICES = [
        ('single', 'Single Phase'),
        ('double', 'Double Phase'),
        ('three', 'Three Phase'),
    ]
    meter_number = models.IntegerField(null=True, unique=True)  # Meter number should be unique
    meter_type = models.CharField(max_length=10, choices=METER_TYPE_CHOICES, null=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True)  # Many-to-one to Consumer

    def __str__(self):
        return str(self.meter_number)


class MeterReading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='readings',null=True)  # Link to Meter
    new_reading = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # New meter reading
    last_reading = models.DecimalField(max_digits=10, decimal_places=2, null=True) 
    meter_status = models.BooleanField(default=True, null=True)  # Active (True) or Not (False)
    processed = models.BooleanField(default=False, null=True)
    reading_date = models.DateField(null=True)
    meter_image = models.ImageField(upload_to='meter_images/', blank=True, null=True)

    def __str__(self):
        return f"Meter: {self.meter.meter_number}, Reading: {self.new_reading}"

