from django import forms
from .models import Consumer
from users.models import User  # If you're using Django's built-in User model

class ConsumerRegistrationForm(forms.ModelForm):
    # You may also want to include fields for the User model like email and password
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Consumer
        fields = ['consumer_number','consumer_name', 'consumer_address', 'consumer_tariff', 'consumer_division']

    def save(self, commit=True):
        # Create the associated User object
        user = User.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_consumer = True
        user.save()
        
        # Create the consumer object linked to the newly created user
        consumer = super().save(commit=False)
        consumer.user = user  # Associate the user with the consumer
        
        if commit:
            consumer.save()
        
        return consumer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'id': 'id_password'})
