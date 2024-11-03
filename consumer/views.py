import math
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from bill.models import Bill
from consumer.models import Consumer
from consumer.utils import consumer_required
from meterreader.models import Meter, MeterReading
from payment.models import Payment
from django.contrib import messages

from datetime import datetime, timedelta

from payment.models import Payment

from django.utils import timezone
from datetime import timedelta
@consumer_required
def dashboard(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    bill = Bill.objects.filter(meter__consumer=consumer).first()
    return render(request, 'consumer/profile_consumer.html', {'bill': bill,'consumer':consumer})
# 1. Payment History
@consumer_required
def payment_history(request):
    consumer = request.user.consumer  # Assuming each user has one Consumer record
    payments = Payment.objects.filter(bill__meter__consumer=consumer).order_by('-payment_date')  # Filter payments for this consumer
    return render(request, 'consumer/payment_history.html', {'payments': payments,'consumer':consumer})

# 2. Bill History
@consumer_required
def bill_history(request):
    consumer = request.user.consumer
    bills = Bill.objects.filter(meter__consumer=consumer).order_by('-billmonth')
    return render(request, 'consumer/bill_history.html', {'bills': bills,'consumer':consumer})

# 3. Show Current Bill
@consumer_required
def current_bill(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    try:
        current_bill = Bill.objects.filter(meter__consumer=consumer, paid=False).latest('billmonth')
        reading = MeterReading.objects.filter(meter=current_bill.meter).latest('reading_date')
    except Bill.DoesNotExist:
        messages.error(request, 'No current unpaid bill found')
        current_bill = None
        reading = None  # Ensure reading is None if no bill found
    
    return render(request, 'consumer/show_bill.html', {'current_bill': current_bill, 'meter_reading': reading})


# 4. Print Current Month Bill
@consumer_required
def print_current_bill(request):
    consumer = request.user.consumer
    try:
        bill = Bill.objects.filter(meter__consumer=consumer).latest('billmonth')
    except Bill.DoesNotExist:
        messages.error(request, 'not found')
        bill = None
    return render(request, 'print_bill.html', {'bill': bill})

# 5. Pay Your Bills Now
@consumer_required
def pay_bills_now(request):
    consumer = request.user.consumer
    pending_bills = Bill.objects.filter(meter__consumer=consumer, paid=False)
    return render(request, 'pay_bills.html', {'pending_bills': pending_bills})



@consumer_required
def pay_bill_demo(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    try:
        today = timezone.now()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Filter for unpaid bills within the current month
        bill = Bill.objects.filter(
        meter__consumer=consumer,
        billmonth__range=(start_of_month, end_of_month),
        paid=False
            ).latest('billmonth')
    except Bill.DoesNotExist:
        return HttpResponse("No unpaid bills found")

    
    # Example: Generating a unique transaction reference number
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Generate pp_TxnRefNo with a prefix 'T'
    pp_txn_ref_no = f"T{current_time}"
    
    # pp_TxnDateTime is the current time
    pp_txn_date_time = current_time
    
    # pp_TxnExpiryDateTime is 24 hours after the current time
    pp_txn_expiry_date_time = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d%H%M%S')

    #txn_ref_no = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().hex)[:6]}"
    if settings.DEBUG:
        pp_amount = math.floor(bill.payableamount / 100) * 100  # Rounds down to the nearest hundred
    else:
        pp_amount = bill.payableamount * 100  # Minor units for production
    pp_currency = 'PKR'  # Currency
    pp_bill_reference = bill.id  # Example Bill Reference
    pp_description = 'Electricity bill payment'  # Transaction Description
    # Get the current timestamp for txnDateTime and txnExpiryDateTime
    # txn_date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    # txn_expiry_date_time = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d%H%M%S")
    
    # Pass these values to the template
    context = {
        'pp_amount': pp_amount,
        'pp_currency': pp_currency,
        'txn_date_time': pp_txn_date_time,
        'txn_expiry_date_time': pp_txn_expiry_date_time,
        'pp_bill_reference': pp_bill_reference,
        'pp_description': pp_description,
        'pp_txn_ref_no': pp_txn_ref_no,
    }
    return render(request, 'consumer/test2.html',context)
