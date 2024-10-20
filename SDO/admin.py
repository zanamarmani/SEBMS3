# consumer/admin.py

from django.contrib import admin
from .models import Tariff

from .models import sdo_profile

@admin.register(sdo_profile)
class SDOProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'office_location', 'joining_date']
    search_fields = ['first_name', 'last_name']
@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('tariff_type', 'price_100', 'price_200', 'price_300', 'price_above')
    search_fields = ('tariff_type',)
    list_filter = ('tariff_type',)
