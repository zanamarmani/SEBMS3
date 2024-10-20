from django.shortcuts import render
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
