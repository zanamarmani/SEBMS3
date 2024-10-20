from datetime import timezone
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
import hashlib
import requests
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

from bill.models import Bill
# Create your views here.
def payment_gateway(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'pay_online.html', {'bill': bill})

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
import hashlib
import requests
from django.conf import settings

def generate_hash(merchant_id, password, integrity_salt, amount, order_ref):
    string_to_hash = f"{merchant_id}:{password}:{amount}:{order_ref}:{integrity_salt}"
    return hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()

def jazzcash_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    # Access the consumer through the meter associated with the bill
    consumer = bill.meter.consumer  # Updated line

    amount = bill.payableamount  # Assuming this is the correct field for the amount
    order_ref = str(bill.id) + str(timezone.now().timestamp())
    merchant_id = settings.JAZZCASH_MERCHANT_ID
    password = settings.JAZZCASH_PASSWORD
    integrity_salt = settings.JAZZCASH_INTEGRITY_SALT

    hash = generate_hash(merchant_id, password, integrity_salt, amount, order_ref)

    # JazzCash API URL
    jazzcash_url = "https://sandbox.jazzcash.com.pk/CustomerPortal/API/PaymentRequest.php"

    payload = {
        "pp_MerchantID": merchant_id,
        "pp_Password": password,
        "pp_Amount": int(amount * 100),  # Amount in Paisas (multiply by 100)
        "pp_TxnRefNo": order_ref,
        "pp_Description": f"Bill Payment for {consumer.consumer_number}",
        "pp_ReturnURL": "http://127.0.0.1:8000/payment_success/",  # Replace with your success URL
        "pp_SecureHash": hash,
    }

    response = requests.post(jazzcash_url, data=payload)

    if response.status_code == 200:
        return HttpResponseRedirect(response.json().get('pp_AuthURL'))
    else:
        return render(request, 'payment_failed.html', {'error': response.text})


def payment_success(request):
    # Update bill status based on returned transaction details
    return render(request, 'payment_success.html')

def payment_failed(request):
    # Show an error page
    return render(request, 'payment_failed.html')
