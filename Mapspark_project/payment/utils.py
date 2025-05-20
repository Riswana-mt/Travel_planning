# payments/utils.py

from django.conf import settings
import hashlib
import hmac
import base64
import json

def verify_paypal_webhook_signature(request_body, headers):
    """
    Verify that the webhook notification is truly from PayPal
    """
    webhook_event = json.loads(request_body)
    
    # Get headers
    transmission_id = headers.get('Paypal-Transmission-Id')
    timestamp = headers.get('Paypal-Transmission-Time')
    webhook_id = settings.PAYPAL_WEBHOOK_ID  # Store this in settings
    event_body = request_body
    
    # Get signature from headers
    actual_signature = headers.get('Paypal-Transmission-Sig')
    
    # Create validation signature
    expected_sig_base = f"{transmission_id}|{timestamp}|{webhook_id}|{hashlib.sha256(event_body).hexdigest()}"
    hmac_digest = hmac.new(
        settings.PAYPAL_WEBHOOK_KEY.encode('utf-8'),  # Store this in settings
        expected_sig_base.encode('utf-8'),
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hmac_digest).decode('utf-8')
    
    # Verify
    return hmac.compare_digest(actual_signature, expected_signature)