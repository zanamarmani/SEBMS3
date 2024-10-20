# sdo_dashboard/context_processors.py
from bill.models import Bill

def bill_processor(request):
    # Get the first tariff or return None if no tariffs exist
    bills = Bill.objects.first()  
    return {'bills':bills }
