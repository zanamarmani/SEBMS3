from django.shortcuts import render, get_object_or_404, redirect
from bill.models import Bill
from consumer.models import Consumer
from consumer.utils import consumer_required
from meterreader.models import Meter, MeterReading
from payment.models import Payment
from django.contrib import messages

@consumer_required
def dashboard(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    return render(request, 'profile_consumer.html', {'consumer': consumer})
# 1. Payment History
@consumer_required
def payment_history(request):
    consumer = request.user.consumer  # Assuming each user has one Consumer record
    payments = Payment.objects.filter(bill__meter__consumer=consumer)
    return render(request, 'payment_history.html', {'payments': payments})

# 2. Bill History
@consumer_required
def bill_history(request):
    consumer = request.user.consumer
    bills = Bill.objects.filter(meter__consumer=consumer).order_by('-billmonth')
    return render(request, 'bill_history.html', {'bills': bills})

# 3. Show Current Bill
@consumer_required
def current_bill(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    try:
        current_bill = Bill.objects.filter(meter__consumer=consumer, paid=False).latest('billmonth')
        reading = get_object_or_404(MeterReading, meter=current_bill.meter)
        meter_reading = reading.reading_date
        print(meter_reading)
    except Bill.DoesNotExist:
        messages.error(request, 'not found')
        current_bill = None
    return render(request, 'show_bill.html', {'current_bill': current_bill,'meter_reading': reading})

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



def pay_bill_demo(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    try:
        bill = Bill.objects.filter(meter__consumer=consumer).latest('billmonth')
    except Bill.DoesNotExist:
        bill = None
    return render(request, 'test.html',{'bill': bill})
