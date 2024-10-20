from django.db import models

from bill.models import Bill

# Create your models here.
class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,null=True)  # Foreign key to Bill
    bank_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Bank charges
    arrears_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Arrears charges

    def __str__(self):
        return f'Payment for Bill {self.bill.id}'
