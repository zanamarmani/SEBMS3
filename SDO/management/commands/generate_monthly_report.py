from django.core.management.base import BaseCommand
from django.db.models import Sum
from bill.models import Bill
from payment.models import Payment
from SDO.models import MonthlyReport
from datetime import date

class Command(BaseCommand):
    help = 'Generate a monthly report'

    def handle(self, *args, **kwargs):
        # Define the month and year for the report
        report_month = date.today().replace(day=1)
        
        # Calculate the total bills, units, and amounts
        total_bills_generated = Bill.objects.filter(billmonth__month=report_month.month, billmonth__year=report_month.year).count()
        total_units_consumed = Bill.objects.filter(billmonth__month=report_month.month, billmonth__year=report_month.year).aggregate(Sum('unitsconsumed'))['unitsconsumed__sum'] or 0
        total_amount_payable = Bill.objects.filter(billmonth__month=report_month.month, billmonth__year=report_month.year).aggregate(Sum('payableamount'))['payableamount__sum'] or 0
        total_amount_paid = Payment.objects.filter(payment_date__month=report_month.month, payment_date__year=report_month.year).aggregate(Sum('total_amount_paid'))['total_amount_paid__sum'] or 0
        total_arrears = Bill.objects.filter(billmonth__month=report_month.month, billmonth__year=report_month.year).aggregate(Sum('arrears'))['arrears__sum'] or 0

        # Create or update the MonthlyReport entry for this month
        report, created = MonthlyReport.objects.update_or_create(
            report_month=report_month,
            defaults={
                'total_bills_generated': total_bills_generated,
                'total_units_consumed': total_units_consumed,
                'total_amount_payable': total_amount_payable,
                'total_amount_paid': total_amount_paid,
                'total_arrears': total_arrears,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Monthly report for {report_month} created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Monthly report for {report_month} updated successfully."))
