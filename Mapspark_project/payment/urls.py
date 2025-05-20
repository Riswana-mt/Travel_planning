# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/create-paypal-order/', views.create_paypal_order, name='create_paypal_order'),
    #path('api/execute-payment/', views.execute_payment, name='execute_payment'),
    #path('payment-success/', views.payment_success, name='payment_success'),
    #path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('paypal-webhook/', views.payment_webhook, name='paypal_webhook'),


    path('create-payment/<int:booking_id>/', views.create_payment, name='create_payment'),
    path('execute-payment/', views.execute_payment, name='execute_payment'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
]