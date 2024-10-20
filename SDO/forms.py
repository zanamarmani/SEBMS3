# forms.py
from django import forms


from .models import Tariff


from .models import Tariff,sdo_profile

from django.contrib.auth.forms import UserCreationForm
from users.models import User  # Assuming you have a custom User model



class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['tariff_type', 'price_100', 'price_200', 'price_300', 'price_above']
class SDOProfileForm(forms.ModelForm):
    class Meta:
        model = sdo_profile
        fields = ['first_name', 'last_name', 'office_location', 'joining_date']

class SDOProfileCreateForm(forms.ModelForm):
    class Meta:
        model = sdo_profile
        fields = ['user', 'first_name', 'last_name', 'office_location', 'joining_date']

# forms.py


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('office_staff', 'Office Staff'),
        ('sdo', 'SDO'),
        ('meter_reader', 'Meter Reader'),
        ('consumer', 'Consumer'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select, label='Role')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'role')

    def clean(self):
        cleaned_data = super().clean()
        selected_role = cleaned_data.get('role')

        # Reset all role fields to False initially
        cleaned_data['is_office_staff'] = False
        cleaned_data['is_sdo'] = False
        cleaned_data['is_meter_reader'] = False
        cleaned_data['is_consumer'] = False

        # Set the selected role to True
        if selected_role == 'office_staff':
            cleaned_data['is_office_staff'] = True
        elif selected_role == 'sdo':
            cleaned_data['is_sdo'] = True
        elif selected_role == 'meter_reader':
            cleaned_data['is_meter_reader'] = True
        elif selected_role == 'consumer':
            cleaned_data['is_consumer'] = True

        return cleaned_data


