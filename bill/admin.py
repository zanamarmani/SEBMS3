from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['meter', 'billmonth', 'duedate', 'unitsconsumed', 'payableamount', 'paid']
    list_filter = ['billmonth', 'paid']
    search_fields = ['meter__meter_number', 'consumer__consumer_name']
