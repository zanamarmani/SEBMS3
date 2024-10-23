# forms.py
from django import forms
from .models import OfficeStaff
from users.models import User

class OfficeStaffForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )
    office_location = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter office location'})
    )
    joining_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = OfficeStaff
        fields = ['first_name', 'last_name', 'office_location', 'joining_date']

    # class Meta:
    #     model = OfficeStaff
    #     fields = ['user', 'first_name', 'last_name', 'office_location', 'joining_date']
