# utils.py (or wherever your utility functions are)
from django.shortcuts import render
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
    labels = ['december','junuary','february','march','april','may','june','july','august','september','october','november']
    total_bills = [4000,3500,405,1008,1500,2300,4500,6907,2778,2943,910,454]
    paid_bills =  [3500,2000,400,1095,1400,2300,3050,6812,1278,2323,190,400]

    return JsonResponse({
        'labels': labels,
        'total_bills': total_bills,
        'paid_bills': paid_bills,
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