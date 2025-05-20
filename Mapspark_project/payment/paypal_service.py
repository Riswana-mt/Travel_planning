# paypal_service.py
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from django.conf import settings

class PayPalClient:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_SECRET_KEY
        
        if settings.PAYPAL_MODE == 'sandbox':
            self.environment = SandboxEnvironment(
                client_id=self.client_id, 
                client_secret=self.client_secret
            )
        else:
            self.environment = LiveEnvironment(
                client_id=self.client_id, 
                client_secret=self.client_secret
            )
            
        self.client = PayPalHttpClient(self.environment)