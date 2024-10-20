from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bill', 'bank_charges', 'arrears_charges']
    search_fields = ['bill__meter__meter_number']
