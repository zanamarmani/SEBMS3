# utils.py (or wherever your utility functions are)
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
from collections import defaultdict
import calendar
from django.utils import timezone
from payment.models import Payment
from datetime import datetime
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def calculate_bill(consumed_units, tariff):
    # Check if a valid tariff exists
    if not tariff:
        raise ValueError("Tariff not found. Please set the tariff in the SDO dashboard.")

    # Initialize total bill
    total_bill = 0
    
    # Pricing tiers based on your Tariff model fields
    price_tiers = [
        (100, tariff.price_100),   # First 100 units
        (100, tariff.price_200),   # Next 100 units (101-200)
        (100, tariff.price_300),   # Next 100 units (201-300)
        (float('inf'), tariff.price_above)  # Above 300 units
    ]
    
    # Calculate the bill based on consumed units and the price tiers
    for limit, price_per_unit in price_tiers:
        if consumed_units > limit:
            total_bill += limit * price_per_unit
            consumed_units -= limit
        else:
            total_bill += consumed_units * price_per_unit
            break
    
    return total_bill

from django.http import JsonResponse
from bill.models import Bill  # Assuming you have a Bill model that tracks bills

def bills_data(request):
    total_bills = Bill.objects.all().count()
    paid_bills = Bill.objects.filter(paid=True).count()  # Assuming 'status' field exists

    data = {
        'total_bills': total_bills,
        'paid_bills': paid_bills,
        'labels': ['Total Bills', 'Paid Bills']
    }

    return JsonResponse(data)


def line_chart(request):
    # Initialize dictionaries to store monthly bill counts
    total_bills_dict = defaultdict(int)
    paid_bills_dict = defaultdict(int)
    unpaid_bills_dict = defaultdict(int)
    
    # Query all bills and group by month
    bills = Bill.objects.all()
    
    for bill in bills:
        if not bill.billmonth:
            continue  # Skip bills without a bill month
        
        month_name = DateFormat(bill.billmonth).format('F')  # Convert to month name
        total_bills_dict[month_name] += 1  # Increment count for total bills
        
        if bill.paid:
            paid_bills_dict[month_name] += 1  # Increment count for paid bills
        else:
            unpaid_bills_dict[month_name] += 1  # Increment count for unpaid bills
    
    # Ensure all months are included, even with zero values
    labels = [calendar.month_name[i] for i in range(1, 13)]
    total_bills = [total_bills_dict[month] for month in labels]
    paid_bills = [paid_bills_dict[month] for month in labels]
    unpaid_bills = [unpaid_bills_dict[month] for month in labels]
    
    # Debugging: Print the data to console (optional)
    print("Total Bills:", total_bills)
    print("Paid Bills:", paid_bills)
    print("Unpaid Bills:", unpaid_bills)
    
    return JsonResponse({
        'labels': labels,
        'total_bills': total_bills,
        'paid_bills': paid_bills,
        'unpaid_bills': unpaid_bills,
    })
def bill_progress_view(request):
    # Assuming you have data for total bills, paid, and unpaid bills
    total_bills = Bill.objects.all().count()
    paid_bills = Bill.objects.filter(paid=True).count()
    # total_bills = 100
    # paid_bills = 60
    unpaid_bills = total_bills - paid_bills
    
    return JsonResponse({
        'total_bills': total_bills,
        'paid_bills': paid_bills,
        'unpaid_bills': unpaid_bills,
    })


def payment_data(request):
    # Get the current year for filtering
    current_year = timezone.now().year
    
    # Initialize monthly totals
    monthly_totals = []
    monthly_paid_totals = []
    monthly_unpaid_totals = []

    # Loop through each month to calculate totals
    for month in range(1, 13):
        # Total amount (paid + unpaid) for the month
        month_total = Payment.objects.filter(
            payment_date__year=current_year,
            payment_date__month=month
        ).aggregate(total=Sum('total_amount_paid'))['total'] or 0

        # Paid amount for the month
        month_paid_total = Payment.objects.filter(
            payment_date__year=current_year,
            payment_date__month=month,
            bill__paid=True  # assuming the Bill model has a 'paid' boolean field
        ).aggregate(total=Sum('total_amount_paid'))['total'] or 0

        # Unpaid amount for the month
        month_unpaid_total = month_total - month_paid_total

        # Append data to lists
        monthly_totals.append(month_total)
        monthly_paid_totals.append(month_paid_total)
        monthly_unpaid_totals.append(month_unpaid_total)
    
    # Yearly totals
    yearly_total = sum(monthly_totals)
    yearly_paid_total = sum(monthly_paid_totals)
    yearly_unpaid_total = sum(monthly_unpaid_totals)

    # Prepare data for JSON response
    data = {
        'months': [calendar.month_name[month] for month in range(1, 13)],
        'monthly_totals': monthly_totals,
        'monthly_paid_totals': monthly_paid_totals,
        'monthly_unpaid_totals': monthly_unpaid_totals,
        'yearly_total': yearly_total,
        'yearly_paid_total': yearly_paid_total,
        'yearly_unpaid_total': yearly_unpaid_total,
    }
    
    return JsonResponse(data)



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
