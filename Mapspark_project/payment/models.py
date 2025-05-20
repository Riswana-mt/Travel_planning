from django.db import models

# Create your models here.


# payments/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

from django.db import models

from django.db import models
from hotel.models import HotelBooking  # or whichever model you're using

class PaymentTransaction(models.Model):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (REFUNDED, 'Refunded'),
    ]
    
    booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE)  # Changed from 'product'
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"





from paypal.standard.ipn.models import PayPalIPN

def update_payment_status(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'Completed':
        try:
            transaction = PaymentTransaction.objects.get(payment_id=ipn_obj.txn_id)
            transaction.status = PaymentTransaction.COMPLETED
            transaction.save()
        except PaymentTransaction.DoesNotExist:
            pass

# Connect the signal
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received

receiver(valid_ipn_received)(update_payment_status)

