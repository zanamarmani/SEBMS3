from django import forms
from .models import Meter

class MeterAssignmentForm(forms.ModelForm):
    consumer_number = forms.CharField(label="Consumer Number", required=True)

    class Meta:
        model = Meter
        fields = ['meter_number', 'meter_type']

    def __init__(self, *args, **kwargs):
        # Remove 'consumer' from kwargs if present to avoid the error
        self.consumer = kwargs.pop('consumer', None)
        super(MeterAssignmentForm, self).__init__(*args, **kwargs)

    def clean_meter_number(self):
        meter_number = self.cleaned_data.get('meter_number')
        if Meter.objects.filter(meter_number=meter_number).exists():
            raise forms.ValidationError("A meter with this number already exists. Please enter a unique meter number.")
        return meter_number
