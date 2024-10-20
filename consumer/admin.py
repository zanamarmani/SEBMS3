from django.contrib import admin
from .models import Consumer

@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ['consumer_number', 'consumer_name', 'consumer_division', 'approved']
    list_filter = ['approved', 'consumer_division']
    search_fields = ['consumer_number', 'consumer_name']

