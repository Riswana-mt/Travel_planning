from django.contrib import admin

# Register your models here.
# payments/admin.py

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)





from django.contrib import admin
from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment_id', 'order_id', 'booking__id')
    readonly_fields = ('created_at', 'updated_at')
    
    # If you want to show booking details
    fieldsets = (
        (None, {
            'fields': ('booking', 'status', 'amount')
        }),
        ('Payment Details', {
            'fields': ('payment_id', 'order_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )