from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'city_from', 'city_to', 'weight', 'delivery_type', 'cost', 'created_at')
    list_filter = ('delivery_type',)
