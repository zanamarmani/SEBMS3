# consumer/models.py

from django.db import models
from users.models import User
from decimal import Decimal
class Tariff(models.Model):
    # Define the different types of tariffs
    TARIFF_CHOICES = [
        ('domestic', 'Domestic'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ]
    
    tariff_type = models.CharField(max_length=10, choices=TARIFF_CHOICES)
    
    # Fields to hold price tiers for each tariff
    price_100 = models.DecimalField(max_digits=10, decimal_places=2,default=3)  # Price for first 100 units
    price_200 = models.DecimalField(max_digits=10, decimal_places=2,default=4)  # Price for 100-200 units
    price_300 = models.DecimalField(max_digits=10, decimal_places=2,default=5)  # Price for 200-300 units
    price_above = models.DecimalField(max_digits=10, decimal_places=2,default=6)  # Price for units above 300
    
    def __str__(self):
        return self.get_tariff_type_display()  # Display readable name in admin

    class Meta:
        verbose_name_plural = 'Tariffs'

class sdo_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)  # One-to-one with User
    first_name = models.CharField(max_length=100,null=True)  # First name
    last_name = models.CharField(max_length=100,null=True,blank=True)  # Last name
    office_location = models.CharField(max_length=255,null=True)  # Office location
    joining_date = models.DateField(null=True)  # Joining date

    def __str__(self):
        return f'SDO: {self.first_name} {self.last_name}'




class MonthlyReport(models.Model):
    month = models.PositiveIntegerField(default=None)
    year = models.PositiveIntegerField(default=None, null=True)
    total_bills_generated = models.PositiveIntegerField(default=0)
    total_units_consumed = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount_payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_consumers = models.IntegerField(default=0)
    total_office_staff = models.IntegerField(default=0)
    total_meter_readers = models.IntegerField(default=0)
    total_meter_assigned = models.IntegerField(default=0)
    # Add other fields as needed

    class Meta:
        unique_together = ('month', 'year')

    def __str__(self):
        return f"Report for {self.month}/{self.year}"