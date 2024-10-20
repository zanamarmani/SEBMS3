from django.contrib import admin
from .models import OfficeStaff

@admin.register(OfficeStaff)
class OfficeStaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'office_location', 'joining_date']
    search_fields = ['first_name', 'last_name']
