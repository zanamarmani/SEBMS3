from django.db import models

from bill.models import Bill

# Create your models here.
class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE,null=True)  # Foreign key to Bill
    bank_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Bank charges
    arrears_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Arrears charges
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total amount paid
    payment_date = models.DateField(auto_now_add=True,null=True)  # Payment date
    txn_id = models.CharField(max_length=255, null=True, blank=True) # Transaction ID
    

    def __str__(self):
        return f'Payment for Bill {self.bill.id}'
