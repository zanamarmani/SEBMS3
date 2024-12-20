from decimal import Decimal
from uuid import uuid4
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic import ListView
from SEBMS import settings

from bill.views import calculate_amount_due, calculate_average_units
from consumer.forms import ConsumerRegistrationForm
from consumer.models import Consumer
from meterreader.forms import MeterAssignmentForm
from meterreader.models import Meter, MeterReading
from officestaff.forms import OfficeStaffForm
from officestaff.models import OfficeStaff
from officestaff.utils import officestaff_required
from users.models import User
from bill.models import Bill
from SDO.models import Tariff
from .firebase_utils import fetch_meter_list
from datetime import date, datetime, timedelta
import os
from django.core.files import File
import requests
from io import BytesIO

from django.db import transaction

from django.utils.dateparse import parse_date

@officestaff_required
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

  
@officestaff_required
def RegisterConsumer(request):
    tariffs=Tariff.tariff_type
    return render(request, 'RegisterConsumer.html',{'tariffs':tariffs})
# officeStaff/views.py


@officestaff_required
def register_consumer(request):
    if request.method == 'POST':
        form = ConsumerRegistrationForm(request.POST)
        if form.is_valid():
            try:
             form.save()
            except:
                messages.error(request, 'Failed to Register Consumer try again with different email')
                return redirect('officestaff:registerconsumer')  # Redirect to a success page or desired location
            return redirect('officestaff:dashboard')  # Redirect to a success page or desired location
        else:
            messages.error(request, 'Failed to Register try different email or consumer number')
    else:
        form = ConsumerRegistrationForm()

    return render(request, 'RegisterConsumer.html', {'form': form})

@officestaff_required
def list_consumers(request):
    consumers = Consumer.objects.all()

    # Get filters from request
    consumer_name = request.GET.get('consumer_name', '')
    consumer_number = request.GET.get('consumer_number', '')
    consumer_division = request.GET.get('consumer_division', '')
    consumer_tariff = request.GET.get('consumer_tariff', '')

    # Apply filters if present
    if consumer_name:
        consumers = consumers.filter(consumer_name__icontains=consumer_name)
    if consumer_number:
        consumers = consumers.filter(consumer_number__icontains=consumer_number)
    if consumer_division:
        consumers = consumers.filter(consumer_division=consumer_division)
    if consumer_tariff:
        consumers = consumers.filter(consumer_tariff__tariff_type=consumer_tariff)

    title = "Consumer"
    context = {
        "consumers": consumers,
        "title": title,
        "consumer_name": consumer_name,
        "consumer_number": consumer_number,
        "consumer_division": consumer_division,
        "consumer_tariff": consumer_tariff,
    }
    return render(request, 'list_consumers.html', context)

@officestaff_required
def all_readings(request):
    month = request.GET.get('month')
    meter_number = request.GET.get('meter_number')
    
    readings = MeterReading.objects.all()

    # Filter by month (if provided)
    if month:
        # Convert the month string to a date object to filter by the month
        month_date = parse_date(month + "-01")
        readings = readings.filter(reading_date__year=month_date.year, reading_date__month=month_date.month)

    # Filter by meter number (if provided)
    if meter_number:
        readings = readings.filter(meter__meter_number=meter_number)
    title ="All Readings"
    return render(request, 'all_readings.html', {'readings': readings,'title':title})


@officestaff_required
def Get_All_Readings(request):
    # Fetch meter readings from Firebase
    meter_readings = fetch_meter_list()
    # Fetch all bills to display on the dashboard
    title="Meter Readings"
    return render(request, 'all_readings.html', {'meter_readings': meter_readings, 'title':title})


@officestaff_required
def save_meter_data_to_db(request):
    meter_data_list = fetch_meter_list()

    for meter_data in meter_data_list:
        date_str = meter_data.get('date', None)
        meter_serial_no = meter_data.get('serial_no', None)
        meter_image_url = meter_data.get('meterImage', None)
        reading = meter_data.get('reading', None)
        status = meter_data.get('isActive', False)

        if not date_str or not meter_serial_no or not reading:
            continue  # Skip if essential data is missing

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            reading = int(round(float(reading)))
        except (ValueError, TypeError):
            continue  # Skip if data is invalid

        try:
            # Get or skip if the meter doesn't exist
            meter = Meter.objects.filter(meter_number=meter_serial_no).first()
            if not meter:
                continue

            # Check if the reading already exists
            if MeterReading.objects.filter(meter=meter, reading_date=date_obj).exists():
                continue

            # Download the image from Firebase if available
            image_file = None
            if meter_image_url:
                try:
                    response = requests.get(meter_image_url, stream=True)
                    if response.status_code == 200:
                        image_filename = f"{uuid4()}.jpg"
                        image_content = BytesIO(response.content)
                        image_file = File(image_content, name=image_filename)
                    else:
                        print(f"Failed to download image: HTTP status {response.status_code}")
                except Exception as e:
                    print(f"Failed to download image: {e}")

            # Get the last reading, default to 500 if no prior readings exist
            last_reading_record = MeterReading.objects.filter(meter=meter).order_by('-reading_date').first()
            last_reading = last_reading_record.new_reading if last_reading_record else 500

            # DEBUG: Log what's happening before creating the object
            print(f"Meter image URL: {meter_image_url}")
            print(f"Saving new reading for meter: {meter_serial_no}, Date: {date_obj}")

            # Save the new reading
            meter_reading = MeterReading.objects.create(
                meter=meter,
                last_reading=last_reading,
                new_reading=reading,
                meter_status=status,
                reading_date=date_obj,
                processed=False
            )

            # Save the image if it exists
            if image_file:
                meter_reading.meter_image.save(image_filename, image_file)
            else:
                print("No image file available; skipping image save.")
                
        except Exception as e:
            print(f"Error while saving meter reading: {e}")

    # Retrieve saved data to display in the template
    meter_list = MeterReading.objects.all()
    return render(request, 'meter_data.html', {'meter_list': meter_list})

# views.py
@officestaff_required
def all_bills(request):
    # Fetch all bills from the database
    bills = Bill.objects.all()
    # Get filter values from the request
    consumer_number = request.GET.get('consumer_number')
    meter_number = request.GET.get('meter_number')
    month = request.GET.get('month')

    # Apply filters based on provided values
    if consumer_number:
        bills = bills.filter(meter__consumer__consumer_number=consumer_number)
    if meter_number:
        bills = bills.filter(meter__meter_number=meter_number)
    if month:
        bills = bills.filter(billmonth__month=month.split("-")[1], billmonth__year=month.split("-")[0])
    title="All Bills"
    return render(request, 'all_bills.html', {'bills': bills, 'title':title})
@officestaff_required
def paid_bills(request):
    # Fetch paid bills from the database
    bills = Bill.objects.filter(paid=True)
    title="Paid Bills"
    return render(request, 'all_bills.html', {'bills': bills,'title':title})
@officestaff_required
def unpaid_bills(request):
    # Fetch unpaid bills from the database
    bills = Bill.objects.filter(paid=False)
    title="Unpaid Bills"
    return render(request, 'all_bills.html', {'bills': bills,'title':title})
from django.views.generic import ListView

@officestaff_required
class TariffListView(ListView):
    model = Tariff
    template_name = 'register_consumer.html'  # Path to your template
    context_object_name = 'tariffs'  # This will be the name of the variable in your template

    def get_queryset(self):
        return Tariff.objects.all()
    

@officestaff_required
def Generate_bill(request):
    # Get all unprocessed meter readings
    meter_readings = MeterReading.objects.filter(processed=False)
    bill_details = []  # For rendering bill data in the template
    newly_generated_bill_ids = []  # Track generated bills for highlighting

    for reading in meter_readings:
        meter = reading.meter  # Get the related Meter object

        # Proceed only if the meter's consumer is approved
        if not (meter.consumer and meter.consumer.approved):
            continue

        consumer = meter.consumer
        tariff = consumer.consumer_tariff
        bill_month = reading.reading_date
        average_units = calculate_average_units(meter)
        
        # Calculate units consumed
        units_consumed = reading.new_reading - reading.last_reading
        if not reading.meter_status or units_consumed < 10:
            units_consumed = average_units
            current_bill = calculate_amount_due(average_units, tariff)
        else:
            current_bill = calculate_amount_due(units_consumed, tariff)
        
        # Calculate payable amount after due date with a 10% late fee
        payable_after_due_date = current_bill * Decimal('1.1')

        # Retrieve and sum unpaid bills to calculate arrears
        previous_unpaid_bills = Bill.objects.filter(meter=meter, paid=False)
        total_arrears = sum(bill.payableamount for bill in previous_unpaid_bills)

        # Calculate the gross total payable amount (current bill + arrears)
        gross_total = current_bill + total_arrears

        # Create a new Bill object
        bill = Bill.objects.create(
            billmonth=bill_month,
            duedate=timezone.now().date() + timedelta(days=15),
            detectionunit=average_units,
            averageunit=average_units,
            units=units_consumed,
            unitsconsumed=units_consumed,
            current_bill=current_bill,
            payableamount=gross_total,  # Gross total including arrears
            payable_after_due_date=payable_after_due_date,
            meter=meter,
            arrears=total_arrears,  # Track the arrears on the bill
            gross_total=gross_total,
            paid=False
        )

        # Track the newly created bill ID for highlighting purposes
        newly_generated_bill_ids.append(bill.id)

        # Mark the meter reading as processed
        reading.processed = True
        reading.save()

        # Collect details for rendering purposes (optional)
        bill_details.append({
            'meter_number': meter.meter_number,
            'consumer_name': consumer.consumer_name,
            'units_consumed': units_consumed,
            'payable_amount': gross_total,  # Total due before late fee
            'payable_after_due_date': payable_after_due_date,
            'gross_total': gross_total,
            'arrears': total_arrears,
            'bill_id': bill.id,
            'current_bill': current_bill,
        })

    # Fetch all bills to render in the template
    all_bills = Bill.objects.all()

    return render(request, 'all_bills.html', {
        'bills': all_bills,
        'newly_generated_bill_ids': newly_generated_bill_ids,
        'bill_details': bill_details  # Optional: Display bill details if needed
    })

@transaction.atomic
def regenerate_bill(request, meter_reading_id):
    # Retrieve the processed meter reading
    meter_reading = get_object_or_404(MeterReading, id=meter_reading_id, processed=True)

    # Retrieve the existing unpaid bill linked to this reading or meter
    existing_bill = Bill.objects.filter(meter=meter_reading.meter, billmonth=meter_reading.reading_date, paid=False).first()

    if existing_bill:
        # Delete the old unpaid bill and reuse its ID
        bill_id = existing_bill.id
        existing_bill.delete()

        # Calculate units consumed
        units_consumed = meter_reading.new_reading - meter_reading.last_reading

        # Fetch the tariff associated with the consumer's meter
        tariff = meter_reading.meter.consumer.consumer_tariff

        # Calculate payable amount based on tariff tiers
        current_bill = calculate_amount_due(units_consumed, tariff)

        # Calculate gross total and late fee if applicable
        gross_total = current_bill + existing_bill.arrears
        payable_after_due_date = gross_total * Decimal('1.05')  # Example late fee

        # Create a new bill with the same ID
        new_bill = Bill.objects.create(
            id=bill_id,
            billmonth=meter_reading.reading_date,
            duedate=existing_bill.duedate,  
            detectionunit=existing_bill.detectionunit,
            averageunit=existing_bill.averageunit,
            units=existing_bill.units,
            unitsconsumed=units_consumed,
            payableamount=gross_total,
            payable_after_due_date=payable_after_due_date,
            meter=meter_reading.meter,
            arrears=existing_bill.arrears,
            gross_total=gross_total,
            current_bill=current_bill,
            paid=False
        )

        # Render success template with bill details
        return render(request, 'regeneration_success.html', {'bill': new_bill})

    else:
        # Render error template if no unpaid bill found
        return render(request, 'regeneration_error.html', {'message': "No unpaid bill to regenerate."})

@officestaff_required
def show_profile(request): 
    try:
        profile = OfficeStaff.objects.filter(user = request.user).first()
        return render(request, 'staff_profile.html', {'profile': profile})
    except:
        return redirect('officestaff:create_office_staff_profile')


@officestaff_required
def create_office_staff_profile(request):
    # Check if the logged-in user already has a profile
    office_staff = OfficeStaff.objects.filter(user=request.user).first()
    
    if office_staff:
        messages.warning(request, "You already have a profile.")
        return render(request,'staff_profile.html',{'profile':office_staff})  # Redirect to list if profile exists

    if request.method == 'POST':
        form = OfficeStaffForm(request.POST)
        if form.is_valid():
            # Save the form without committing to associate it with the user
            office_staff = form.save(commit=False)
            office_staff.user = request.user  # Set the logged-in user
            office_staff.save()  # Save the profile
            messages.success(request, "Office staff profile created successfully.")
            return redirect('officestaff:show_profile')  # Redirect to a list or detail page
    else:
        form = OfficeStaffForm()

    return render(request, 'create_office_staff.html', {'form': form})

@officestaff_required
def edit_office_staff(request):
    # Retrieve the specific OfficeStaff instance or return 404 if not found
    office_staff = OfficeStaff.objects.filter(user= request.user).first()

    if request.method == 'POST':
        form = OfficeStaffForm(request.POST, instance=office_staff)  # Bind the form with existing data
        if form.is_valid():
            form.save()
            return redirect('officestaff:show_profile')  # Redirect to a list or detail view
    else:
        form = OfficeStaffForm(instance=office_staff)  # Load the form with the current data

    return render(request, 'edit_office_staff.html', {'form': form, 'office_staff': office_staff})


@officestaff_required
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

@officestaff_required
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
            return redirect('officestaff:dashboard')

    else:
        form = MeterAssignmentForm()

    return render(request, 'assign_meter.html', {'form': form, 'consumer': consumer, 'error': error})


@officestaff_required
def consumer_profile(request, consumer_id):
    # Get the consumer profile based on the ID passed in the URL
    consumer = get_object_or_404(Consumer, id=consumer_id)
    bill = Bill.objects.filter(meter__consumer_id=consumer_id).first()
    meter = Meter.objects.filter(consumer=consumer).first()
    
    return render(request, 'consumer_profile.html', {'bill': bill,'consumer': consumer, 'meter':meter})

def view_bill_details(request,bill_id): 
    try:
        bill = Bill.objects.filter(id=bill_id).first()
        reading = MeterReading.objects.filter(meter=current_bill.meter).latest('reading_date')
    except Bill.DoesNotExist:
        messages.error(request, 'No current unpaid bill found')
        current_bill = None
        reading = None  # Ensure reading is None if no bill found
    
    return render(request, 'consumer/show_bill.html', {'current_bill': bill, 'meter_reading': reading})