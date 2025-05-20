from django.shortcuts import render

# Create your views here.
# payments/views.py

import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings

from .models import Product, PaymentTransaction
from .paypal_config import get_paypal_client

def product_detail(request, product_id):
    """Display product details with PayPal button"""
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    }
    return render(request, 'payments/product_detail.html', context)

@csrf_exempt
def create_paypal_order(request):
    """API endpoint to create a PayPal order"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        # Get product
        product = get_object_or_404(Product, id=product_id)
        
        # Initialize PayPal client
        paypal = get_paypal_client()
        
        # Create order
        payment = paypal.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payments:payment_success')),
                "cancel_url": request.build_absolute_uri(reverse('payments:payment_cancel'))
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": product.name,
                        "sku": f"product-{product.id}",
                        "price": str(product.price),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(product.price),
                    "currency": "USD"
                },
                "description": product.description
            }]
        })
        
        # Create the payment
        if payment.create():
            # Create transaction record
            transaction = PaymentTransaction.objects.create(
                product=product,
                payment_id=payment.id,
                amount=product.price,
                status=PaymentTransaction.PENDING
            )
            
            # Extract approval URL to redirect the user to PayPal
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return JsonResponse({
                        'id': payment.id,
                        'approval_url': approval_url
                    })
        
        else:
            return JsonResponse({'error': payment.error}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def execute_payment(request):
    """Execute PayPal payment after approval"""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    if not payment_id or not payer_id:
        return JsonResponse({'error': 'Missing payment parameters'}, status=400)
    
    try:
        # Initialize PayPal client
        paypal = get_paypal_client()
        
        # Fetch payment
        payment = paypal.Payment.find(payment_id)
        
        # Execute payment with payer ID
        if payment.execute({"payer_id": payer_id}):
            # Update transaction
            transaction = PaymentTransaction.objects.get(payment_id=payment_id)
            transaction.status = PaymentTransaction.COMPLETED
            transaction.save()
            
            return JsonResponse({
                'success': True,
                'transaction_id': transaction.id
            })
        else:
            return JsonResponse({'error': 'Payment execution failed'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def payment_success(request):
    """Handle successful payment return"""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    if payment_id and payer_id:
        # Process payment
        paypal = get_paypal_client()
        payment = paypal.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            # Update transaction
            transaction = PaymentTransaction.objects.get(payment_id=payment_id)
            transaction.status = PaymentTransaction.COMPLETED
            transaction.save()
            
            return render(request, 'payments/payment_success.html', {
                'transaction': transaction
            })
    
    return render(request, 'payments/payment_error.html')

def payment_cancel(request):
    """Handle canceled payment"""
    return render(request, 'payments/payment_cancel.html')

def payment_webhook(request):
    """Handle PayPal webhooks for payment status updates"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Process webhook data
    # Verify webhook signature and handle different event types
    # Update transaction status accordingly
    
    return JsonResponse({'status': 'success'})









from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from hotel.models import HotelBooking  # Adjust based on your model
from payment.models import PaymentTransaction
import paypalrestsdk

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment(request, booking_id):
    booking = get_object_or_404(HotelBooking, id=booking_id)
    
    # Create a PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": str(booking.total_price),  # Ensure this is a string
                "currency": "USD",  # Change as needed
            },
            "description": f"Payment for Hotel Booking #{booking.id}"
        }],
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed'))
        }
    })
    
    if payment.create():
        # Save transaction to database
        transaction = PaymentTransaction.objects.create(
            booking=booking,
            payment_id=payment.id,
            amount=booking.total_price,
            status=PaymentTransaction.PENDING
        )
        return redirect(payment.links[1].href)  # Redirect to PayPal approval URL
    else:
        return render(request, 'payment_failed.html', {'error': payment.error})

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        # Update transaction status
        transaction = PaymentTransaction.objects.get(payment_id=payment_id)
        transaction.status = PaymentTransaction.COMPLETED
        transaction.payer_id = payer_id
        transaction.save()
        
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html', {'error': payment.error})

def payment_failed(request):
    return render(request, 'payment_failed.html')