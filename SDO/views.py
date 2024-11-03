from django.shortcuts import redirect, render,get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.crypto import get_random_string

from SDO.utils import sdo_required
from bill.models import Bill
from meterreader.models import Meter
from users.models import User
from django.contrib import messages

from .models import Tariff
from .forms import TariffForm

from consumer.models import Consumer
from users.forms import UserForm

from django.contrib.auth.decorators import login_required

from .models import sdo_profile
from .forms import SDOProfileForm,SDOProfileCreateForm

from django.contrib.auth import login
from .forms import CustomUserCreationForm

import logging

logger = logging.getLogger(__name__)

@sdo_required
def dashboard(request):
    # Check if the user has a profile
    profile = sdo_profile.objects.filter(user=request.user).first()

    if not profile:
        pass
        # If the profile doesn't exist, redirect to profile creation page
        #return redirect('SDO:create_sdo_profile')  # Adjust with the actual name of your URL

    # If profile exists, continue with dashboard logic
    tariff = Tariff.objects.first()  # or use specific filters to get a tariff
    consumers = Consumer.objects.count()
    users = User.objects.count()
    office_staffs = User.objects.filter(is_office_staff=True).count()
    meter_readers = User.objects.filter(is_meter_reader=True).count()

    return render(request, 'sdo/dashboard.html', {'users': users,'tariff': tariff,'consumers':consumers,'total_office_staff':office_staffs,'total_users':users,'total_meter_reader':meter_readers})



@sdo_required
def create_office_staff(request):
    if request.method == "POST":
        reference_number = get_random_string(8)
        password = 'officestaff'
        new_office_staff = User.objects.create_user(
            username=reference_number, password=password, is_office_staff=True
        )
        # Optional: Add a success message
        messages.success(request, f"Office staff created with reference number {reference_number} and default password.")
        return redirect('SDO:dashboard')
    return render(request, 'sdo/create_office_staff.html')

@sdo_required
def admin_dashboard(request):
    return render(request, 'sdo/admin_dashboard.html')

@sdo_required
def approve_new_consumers(request):
    consumers = Consumer.objects.filter(approved=False)
    if request.method == 'POST':
        consumer_id = request.POST.get('consumer_id')
        consumer = Consumer.objects.get(id=consumer_id)
        consumer.approved = True
        consumer.save()
        return redirect('SDO:approve_new_consumers')
    title="Approve Consumer"
    return render(request, 'sdo/approve_new_consumers.html', {'consumers': consumers, 'title':title})

@sdo_required
def reject_new_consumers(request):
    if request.method == 'POST' and request.POST.get('action') == 'reject':
        consumer_id = request.POST.get('consumer_id')
        consumer = get_object_or_404(Consumer, id=consumer_id)
        
        # Handle any additional logic for rejected consumers (e.g., deleting, marking as rejected)
        consumer.delete()  # Delete the consumer from the database
        
        return redirect('SDO:approve_new_consumers')  # Redirect back to the same page
    return render(request, 'sdo/approve_new_consumers.html', {'consumers': consumer})
    # return redirect('approve_new_consumers')


# def add_user(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('SDO:show_all_users')
#     else:
#         form = UserForm()
#     return render(request, 'sdo/add_user.html', {'form': form})

@sdo_required
def show_all_consumers(request):
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
    return render(request, 'sdo/show_all_consumers.html', context)


@sdo_required
def consumer_profile(request, consumer_id):
    # Get the consumer profile based on the ID passed in the URL
    consumer = get_object_or_404(Consumer, id=consumer_id)
    
    # Fetch the bill for the current consumer
    bill = Bill.objects.filter(meter__consumer_id=consumer_id).first()
    
    return render(request, 'sdo/profile_consumer.html', {'bill': bill,'consumer': consumer})

@sdo_required
def show_all_users(request):
    # Get filter parameters from GET request
    email_filter = request.GET.get('email', '')
    role_filter = request.GET.get('role', '')

    # Start with all users
    users = User.objects.all()

    # Filter by email if provided
    if email_filter:
        users = users.filter(email__icontains=email_filter)

    # Filter by role
    if role_filter == 'office_staff':
        users = users.filter(is_office_staff=True)
    elif role_filter == 'meter_reader':
        users = users.filter(is_meter_reader=True)
    elif role_filter == 'consumer':
        users = users.filter(is_consumer=True)
    elif role_filter == 'sdo':
        users = users.filter(is_sdo=True)

    # Pass the filters back to the template for display
    title = "Users"
    context = {
        'users': users,
        'title': title,
        'email_filter': email_filter,
        'role_filter': role_filter,
    }
    return render(request, 'sdo/show_all_users.html', context)




@sdo_required
def tariff_list(request):
    # Fetch all tariffs for display
    all_tariffs = Tariff.objects.all()
    title="Tariff List"
    return render(request, 'sdo/tariff_list.html', {'all_tariffs': all_tariffs, 'title':title })



@sdo_required
def all_bills(request):
    # Fetch all bills from the database
    bills = Bill.objects.all()
    title="All Bills"
    return render(request, 'sdo/all_bills.html', {'bills': bills, 'title':title})

@sdo_required
def paid_bills(request):
    # Fetch paid bills from the database
    bills = Bill.objects.filter(paid=True)
    title='Paid Bills'
    return render(request, 'sdo/all_bills.html', {'bills': bills, 'title':title})

@sdo_required
def unpaid_bills(request):
    # Fetch unpaid bills from the database
    bills = Bill.objects.filter(paid=False)
    title='Unpaid Bills'
    return render(request, 'sdo/all_bills.html', {'bills': bills, 'title':title})


@sdo_required
def sdo_dashboard_show_details(request):
    # Count total consumers
    total_consumers = Consumer.objects.all()

    # Count total office staff (assuming 'office_staff' is a role in the User model)
    office_staff = User.objects.filter(is_office_staff=True)

    # Count total meter readers (assuming 'meter_reader' is a role in the User model)
    meter_readers = User.objects.filter(is_meter_reader=True)

    return render(request, 'sdo/show_all_users.html',{'consumers': total_consumers,'office_staff': office_staff,'meter_readers': meter_readers})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tariff
from .forms import TariffForm  # Assuming you create a TariffForm

@sdo_required
def create_or_update_tariff(request):
    if request.method == 'POST':
        form = TariffForm(request.POST)
        if form.is_valid():
            # Check if the tariff already exists based on the tariff_type
            tariff_type = form.cleaned_data['tariff_type']
            existing_tariff = Tariff.objects.filter(tariff_type=tariff_type).first()
            
            if existing_tariff:
                # Update the existing tariff with new data
                for field, value in form.cleaned_data.items():
                    setattr(existing_tariff, field, value)
                existing_tariff.save()
                messages.success(request, f"Tariff of type '{existing_tariff.get_tariff_type_display()}' updated successfully!")
            else:
                # Create new tariff if not found
                form.save()
                messages.success(request, "New tariff created successfully!")
            
            return redirect('SDO:tariff_list')  # Redirect after successful creation or update
    else:
        form = TariffForm()
    return render(request, 'sdo/update_tariff.html', {'form': form})




# View to show the SDO profile
@sdo_required
def sdo_profile_view(request):
    try:
        sdo_profile_instance = sdo_profile.objects.filter(user=request.user).first()
        return render(request, 'sdo/sdo_profile_view.html', {'profile': sdo_profile_instance})
    except:
        return redirect('SDO:create_sdo_profile')  # Render the profile view if the SDO profile does not exist

@sdo_required
def edit_sdo_profile_view(request):
    sdo_profile_instance = get_object_or_404(sdo_profile, user=request.user)
    
    if request.method == 'POST':
        form = SDOProfileForm(request.POST, instance=sdo_profile_instance)
        if form.is_valid():
            form.save()
            return redirect('SDO:sdo_profile')  # Redirect to the profile view after saving
    else:
        form = SDOProfileForm(instance=sdo_profile_instance)
    
    return render(request, 'sdo/edit_sdo_profile.html', {'form': form})

@sdo_required
def create_sdo_profile_view(request):
    if request.method == 'POST':
        form = SDOProfileCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('SDO:sdo_profile')  # Redirect to profile page after creation
    else:
        form = SDOProfileCreateForm()

    return render(request, 'sdo/create_sdo_profile.html', {'form': form})

# views.py


@sdo_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_office_staff = form.cleaned_data['is_office_staff']
            user.is_sdo = form.cleaned_data['is_sdo']
            user.is_meter_reader = form.cleaned_data['is_meter_reader']
            user.is_consumer = form.cleaned_data['is_consumer']
            user.save()
            return redirect('SDO:show_all_users')

    else:
        form = CustomUserCreationForm()

    return render(request, 'sdo/add_user.html', {'form': form})


@sdo_required
def delete_consumer(request, pk):
    # Fetch the consumer by their primary key (id) and ensure they are unapproved
    try:
        # Fetch the consumer by primary key (id) and ensure they are unapproved
        consumer = get_object_or_404(Consumer, pk=pk)
        
        # Log to check if the consumer is found
        print(f"Found consumer: {consumer.consumer_name}")

        # Delete the consumer
        consumer.delete()

        # Add a success message
        messages.success(request, f'Consumer {consumer.consumer_name} has been deleted.')

    except Exception as e:
        # In case of an error, log the error message
        print(f"Error: {e}")
        messages.error(request, 'No consumer matches the given query.')

    # Redirect to a list or dashboard after deletion
    return redirect('SDO:show_all_consumers') 