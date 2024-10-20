from decimal import Decimal
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from SDO.models import Tariff

from consumer.forms import ConsumerRegistrationForm
from consumer.models import Consumer
from meterreader.forms import MeterAssignmentForm
from meterreader.models import Meter, MeterReading
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from officestaff.models import OfficeStaff
from users.models import User

from bill.models import Bill
from SDO.utills import calculate_bill
from datetime import date, datetime, timedelta
from django.core.mail import send_mail


from .firebase_utils import fetch_meter_list 

from django.contrib.auth.decorators import login_required

from bill.views import calculate_amount_due

def Home(request):
    consumers = Consumer.objects.all()# Fetch all consumers from the database
    tariff = Tariff.objects.first()  
    consumers1 = Consumer.objects.count()

    # Count total office staff (assuming 'office_staff' is a role in the User model)
    office_staffs = User.objects.filter(is_office_staff = True).count()
    bills = Bill.objects.count()
    # Count total meter readers (assuming 'meter_reader' is a role in the User model)
    meter_readers = User.objects.filter(is_meter_reader=True).count()  
    return render(request, 'officeStaffHome.html', {'consumers': consumers,'consumers1':consumers1,'total_office_staff':office_staffs,'bills':bills,'total_meter_reader':meter_readers})

  
def RegisterConsumer(request):
    tariffs=Tariff.tariff_type
    return render(request, 'RegisterConsumer.html',{'tariffs':tariffs})
# officeStaff/views.py


def register_consumer(request):
    if request.method == 'POST':
        form = ConsumerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('officestaff:home')  # Redirect to a success page or desired location
        else:
            messages.error(request, 'Failed to Register try different email or consumer number')
    else:
        form = ConsumerRegistrationForm()

    return render(request, 'RegisterConsumer.html', {'form': form})


def list_consumers(request):
    consumers = Consumer.objects.all()
    title="consumer"
    return render(request, 'list_consumers.html', {'consumers': consumers,'title':title})


def all_readings(request):
    readings = MeterReading.objects.all()
    title ="All Readings"
    return render(request, 'all_readings.html', {'readings': readings,'title':title})

def generate_bill(request, meter_number):
    """
    View to generate a bill for a specific consumer based on meter readings.
    """
    consumer = get_object_or_404(Consumer, meter_number=meter_number)
    reading = Meter.objects.filter(meter_number=meter_number).last()  # Get the latest reading

    if not reading:
        messages.error(request, "No meter reading found for this consumer.")
        return redirect('officestaff:consumer_list')

    consumed_units = reading.new_reading - reading.last_reading
    if consumed_units < 0:
        messages.error(request, "Consumed units cannot be negative. Please check meter readings.")
        return redirect('officestaff:consumer_list')

    # Get the consumer's tariff and calculate the bill
    tariff = Tariff.objects.filter(tariff_type=consumer.tariff).first()
    if not tariff:
        messages.error(request, "Tariff not found for this consumer.")
        return redirect('officestaff:list_consumers')

    bill_amount = calculate_bill(consumed_units, tariff)

    # Create a new Bill entry for the current month
    bill = Bill.objects.create(
        consumer=consumer,
        month=date.today(),  # Current month
        amount_due=bill_amount,
        consumed_units=consumed_units,
        paid=False
    )

    messages.success(request, f'Bill for consumer {consumer.name} has been generated successfully!')
    return redirect('officestaff:all_readings')

def Get_All_Readings(request):
    # Fetch meter readings from Firebase
    meter_readings = fetch_meter_list()
    # Fetch all bills to display on the dashboard
    title="Meter Readings"
    return render(request, 'all_readings.html', {'meter_readings': meter_readings, 'title':title})

def save_meter_data_to_db(request):
    """
    Fetch the meter data from Firebase and save it to the local database.
    """
    # Fetch meter data from Firebase
    meter_data_list = fetch_meter_list()

    # Process and save each meter reading into the local database
    for meter_data in meter_data_list:
        meter_serial_no = meter_data.get('serial_no', None)  # Serial number of the meter
        date_str = meter_data.get('date', None)  # Date string
        reading = meter_data.get('reading', None)  # Meter reading value

        if not meter_serial_no or not date_str or not reading:
            continue  # Skip if required data is missing

        # Convert date from string to Python date object
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            continue  # Skip this entry if date is invalid

        try:
            reading = float(reading)  # Convert the reading to float
        except ValueError:
            continue  # Skip this entry if reading is invalid

        reading = int(round(reading))  # Round and convert to integer

        # Retrieve or create the Meter object based on the serial number
        meter = Meter.objects.filter(meter_number=meter_serial_no).first()
        if not meter:
            continue  # If the meter doesn't exist, skip this entry

        # Check if the reading for this meter on this date already exists
        if MeterReading.objects.filter(meter=meter, reading_date=date_obj).exists():
            continue  # Skip if the reading already exists for this meter on this date

        # Retrieve the last reading for this meter using filter() and order by the most recent reading
        last_reading_record = MeterReading.objects.filter(meter=meter).order_by('-reading_date').first()

        last_reading = last_reading_record.new_reading if last_reading_record else 500  # Default last reading if no previous record

        # Save the new MeterReading
        meter_reading = MeterReading.objects.create(
            meter=meter,
            last_reading=last_reading,
            new_reading=reading,
            reading_date=date_obj,
            processed=False
        )

    # After saving, retrieve the saved data to display it
    meter_list = MeterReading.objects.all()
    title = " Fetched Meter Readings"
    # Render the template with the saved meter data
    return render(request, 'meter_data.html', {'meter_list': meter_list ,'title': title})

# views.py

def all_bills(request):
    # Fetch all bills from the database
    bills = Bill.objects.all()
    title="All Bills"
    return render(request, 'all_bills.html', {'bills': bills, 'title':title})

def paid_bills(request):
    # Fetch paid bills from the database
    bills = Bill.objects.filter(paid=True)
    title="Paid Bills"
    return render(request, 'paid_bills.html', {'paid_bills': bills,'title':title})

def unpaid_bills(request):
    # Fetch unpaid bills from the database
    bills = Bill.objects.filter(paid=False)
    title="Unpaid Bills"
    return render(request, 'unpaid_bills.html', {'unpaid_bills': bills,'title':title})
from django.views.generic import ListView

class TariffListView(ListView):
    model = Tariff
    template_name = 'register_consumer.html'  # Path to your template
    context_object_name = 'tariffs'  # This will be the name of the variable in your template

    def get_queryset(self):
        return Tariff.objects.all()
    

def Generate_bill(request):
    # Get all unprocessed meter readings
    meter_readings = MeterReading.objects.filter(processed=False)
    bill_details = []  # For rendering bill data in the template
    newly_generated_bill_ids = []  # Track generated bills for highlighting

    for reading in meter_readings:
        meter = reading.meter  # Get the related Meter object

        if meter.consumer and meter.consumer.approved:
            tariff = meter.consumer.consumer_tariff  # Get the consumer's tariff
        else:
            continue  # Skip if consumer is not approved

        # Calculate units consumed
        units_consumed = reading.new_reading - reading.last_reading

        # Calculate the payable amounts
        payable_amount = calculate_amount_due(units_consumed, tariff)
        payable_after_due_date = payable_amount * Decimal('1.1')  # 10% late fee

        # Create a new Bill object
        bill = Bill.objects.create(
            billmonth=timezone.now().date(),  # Current month
            duedate=timezone.now().date() + timedelta(days=15),  # Due date 15 days later
            detectionunit=Decimal('0.00'),  # Assuming no detection units
            averageunit=Decimal('0.00'),  # Assuming no average units
            units=units_consumed,  # Total units for the bill
            unitsconsumed=units_consumed,  # Units consumed by the meter
            payableamount=payable_amount,  # Amount due before the due date
            payable_after_due_date=payable_after_due_date,  # Amount after due date
            meter=meter,  # Link the meter to the bill
            paid=False  # Initially mark as unpaid
        )

        # Track the newly created bill
        newly_generated_bill_ids.append(bill.id)

        # Mark the meter reading as processed
        reading.processed = True
        reading.save()

        # Collect details for rendering purposes (optional)
        bill_details.append({
            'meter_number': meter.meter_number,
            'consumer_name': meter.consumer.consumer_name,
            'units_consumed': units_consumed,
            'payable_amount': payable_amount,
            'payable_after_due_date': payable_after_due_date,
            'bill_id': bill.id  # Track bill ID for reference
        })

    # Fetch all bills to render in the template
    all_bills = Bill.objects.all()

    return render(request, 'all_bills.html', {
        'bills': all_bills,
        'newly_generated_bill_ids': newly_generated_bill_ids,  # For highlighting new bills
    })


def show_profile(request):
    profile = get_object_or_404(OfficeStaff, user = request.user)
    return render(request, 'staff_profile.html', {'profile': profile})


def update_office_staff_profile(request, pk):

    return render(request, 'update_office_staff_profile.html')


def delete_unapproved_consumer(request, pk):
    # Fetch the consumer by their primary key (id) and ensure they are unapproved
    try:
        # Fetch the consumer by primary key (id) and ensure they are unapproved
        consumer = get_object_or_404(Consumer, pk=pk, approved=False)
        
        # Log to check if the consumer is found
        print(f"Found unapproved consumer: {consumer.consumer_name}")

        # Delete the consumer
        consumer.delete()

        # Add a success message
        messages.success(request, f'Consumer {consumer.consumer_name} has been deleted.')

    except Exception as e:
        # In case of an error, log the error message
        print(f"Error: {e}")
        messages.error(request, 'No unapproved consumer matches the given query.')

    # Redirect to a list or dashboard after deletion
    return redirect('officestaff:list_consumers') 

def assign_meter_view(request):
    consumer = None
    error = None

    if request.method == 'GET' and 'consumer_number' in request.GET:
        consumer_number = request.GET.get('consumer_number')

        try:
            consumer = Consumer.objects.get(consumer_number=consumer_number, approved=True)
        except Consumer.DoesNotExist:
            error = "Consumer not found or not approved."
            consumer = None

        form = MeterAssignmentForm(consumer=consumer)

    elif request.method == 'POST':
        consumer_number = request.POST.get('consumer_number')

        try:
            consumer = Consumer.objects.get(consumer_number=consumer_number, approved=True)
        except Consumer.DoesNotExist:
            error = "Consumer not found or not approved."
            consumer = None

        form = MeterAssignmentForm(request.POST, consumer=consumer)

        if form.is_valid() and consumer:
            meter = form.save(commit=False)
            meter.consumer = consumer
            meter.save()
            return redirect('success_page')

    else:
        form = MeterAssignmentForm()

    return render(request, 'assign_meter.html', {'form': form, 'consumer': consumer, 'error': error})
