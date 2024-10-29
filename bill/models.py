from django.db import models
from meterreader.models import Meter


class Bill(models.Model):
    billmonth = models.DateField(null=True)  # Month of the bill
    duedate = models.DateField(null=True,blank=True)  # Due date for payment
    detectionunit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Detected unit (if any)
    averageunit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Average unit
    units = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Units
    unitsconsumed = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Units consumed
    payableamount = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Amount payable
    payable_after_due_date = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Amount after due date
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE,null=True,blank=True)  # Many-to-one to Meter
    arrears = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    gross_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    current_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paid = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f'Bill for {self.billmonth} (Due: {self.duedate})'
