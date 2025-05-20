# payments/paypal_config.py

import paypalrestsdk
from django.conf import settings

def get_paypal_client():
    """Configure and return PayPal SDK client"""
    paypalrestsdk.configure({
        "mode": settings.sandbox,  # sandbox or live
        "client_id": settings.AU9U37cKS78nWT5nDeFwK12CX6BiLI_N9PcdRqP7efAT9fJkTmlNnbH0bTL4xOXMDox40vJxULMP8Oeg,
        "client_secret": settings.EOuPmfJOBI9XRO_g5ohipmOYzlaUxqcx37vCxHqbjbQNWHB11vCbmpgEhta86_57wlp07I0GYRg5NE7K,
    })
    
    return paypalrestsdk