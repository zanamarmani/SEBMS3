from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  # Use Django's built-in form
from django.urls import reverse  # To dynamically resolve URLs


from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

User = get_user_model()  # Get the custom User model

# Update View for User
class UserUpdateView(UpdateView):
    model = User
    template_name = 'registration/user_update.html'
    fields = ['email', 'is_office_staff', 'is_meter_reader', 'is_sdo', 'is_consumer']
    success_url = reverse_lazy('SDO:show_all_users')  # Redirect to a user list view after update

    def form_valid(self, form):
        # Custom logic for updating roles
        user = form.save(commit=False)
        
        # Example role update logic: Make user a meter reader, remove office staff role


        user.save()
        return super().form_valid(form)

# View for updating password
def update_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Keeps the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'registration/password_update.html', {'form': form})

# Delete View for User
class UserDeleteView(DeleteView):
    model = User
    template_name = 'registration/user_confirm_delete.html'
    success_url = reverse_lazy('SDO:show_all_users')  # Redirect after deletion



def user_login(request):
    # Nested function to handle redirection based on user role
    def redirect_to_dashboard(user):
        if user.is_sdo:
            return redirect('SDO:dashboard')
        elif user.is_superuser:
            return redirect('SDO:dashboard')  
        elif user.is_office_staff:
            return redirect('officestaff:home')
        elif user.is_meter_reader:
            return redirect('meterreader:home')
        elif user.is_consumer:
            return redirect('consumer:dashboard')
        else:
            return HttpResponse("User role not recognized. Please check user roles.")
    
    # If the request is POST, process the form
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_to_dashboard(user)  # Redirect user based on role
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            return render(request, 'users/login.html', {'form': form, 'error': 'Invalid form submission'})
    
    # If the request is GET, render the form
    else:
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

def homePage(request):
    return render(request, 'users/index.html')

def success_page(request):
    return render(request, 'registration/success_page.html')

