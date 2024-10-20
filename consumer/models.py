# consumer/models.py
from django.db import models
from users.models import User
from SDO.models import Tariff
class Consumer(models.Model):
    DIVISION_CHOICES = [
        ('division1', 'Division 1'),
        ('division2', 'Division 2'),
        ('division3', 'Division 3'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)  # One-to-one with User 
    consumer_number = models.CharField(max_length=255, unique=True, null=True)  # Unique consumer number   
    consumer_name = models.CharField(max_length=255,null=True)  # Consumer name
    consumer_address = models.CharField(max_length=255,null=True)  # Consumer address
    consumer_tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE,null=True)  # Foreign key to Tariff
    consumer_division = models.CharField(max_length=255, choices=DIVISION_CHOICES, null=True)  # Consumer division with choices
    approved = models.BooleanField(default=False) 

    def __str__(self):
        return self.consumer_name

