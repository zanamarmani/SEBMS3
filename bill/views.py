from decimal import Decimal
from django.shortcuts import render
from django.db.models import Avg

from bill.models import Bill
# Create your views here.
def calculate_amount_due(units_consumed, tariff):
    if units_consumed <= 100:
        amount_due = units_consumed * tariff.price_100
    elif units_consumed <= 200:
        amount_due = (100 * tariff.price_100) + ((units_consumed - 100) * tariff.price_200)
    elif units_consumed <= 300:
        amount_due = (100 * tariff.price_100) + (100 * tariff.price_200) + ((units_consumed - 200) * tariff.price_300)
    else:
        amount_due = (100 * tariff.price_100) + (100 * tariff.price_200) + (100 * tariff.price_300) + ((units_consumed - 300) * tariff.price_above)
    
    return amount_due




def calculate_average_units(meter, num_bills=None):
    """
    Calculate the average units consumed for a meter based on the last `num_bills`.
    If `num_bills` is None, it calculates the average from all previous bills.
    
    Args:
    - meter: The Meter instance for which to calculate the average.
    - num_bills (optional): The number of recent bills to consider for averaging.

    Returns:
    - Decimal: The average units consumed.
    """
    # Fetch previous bills for the meter
    previous_bills = Bill.objects.filter(meter=meter).order_by('-billmonth')
    
    # Limit to `num_bills` if specified
    if num_bills:
        previous_bills = previous_bills[:num_bills]

    # Calculate the average of units consumed in these bills
    average_units = previous_bills.aggregate(Avg('unitsconsumed'))['unitsconsumed__avg']

    # Return the average units, or 0 if no previous bills are available
    return average_units or Decimal('0.00')

