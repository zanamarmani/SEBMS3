from django.db import models
from users.models import User
# Create your models here.
class OfficeStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)  # One-to-one with User
    first_name = models.CharField(max_length=100,null=True)  # First name
    last_name = models.CharField(max_length=100,null=True)  # Last name
    office_location = models.CharField(max_length=255,null=True)  # Office location
    joining_date = models.DateField(null=True)  # Joining date

    def __str__(self):
        return f'Office Staff: {self.first_name} {self.last_name}'
