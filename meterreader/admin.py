from django.contrib import admin
from .models import Meter

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['meter_number', 'consumer']
    search_fields = ['meter_number', 'consumer__consumer_name']
