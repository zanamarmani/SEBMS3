from django.contrib import admin
from consumer.models import User, Consumer

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_sdo', 'is_office_staff', 'is_meter_reader', 'is_consumer', 'is_staff']
    list_filter = ['is_sdo', 'is_office_staff', 'is_meter_reader', 'is_consumer']
    search_fields = ['email']
    def delete_model(self, request, obj):
        # Delete the related consumer manually
        Consumer.objects.filter(user=obj).delete()
        # Then delete the user
        super().delete_model(request, obj)
