from django.urls import path
from .import views

urlpatterns = [    
     path('search/',views.flight_search_view, name='flight_search'),
     path('check_out/',views.check_out,name="check_out"),
     path('base/',views.base,name="base"),
     path('payment_success/',views.payment_success,name="payment_success"),
     path('traveller_info/',views.traveller_info,name="traveller_info"),
     path('search/payment/',views.payment,name="payment"),
     path('confirmation/',views.confirmation,name="confirmation")
]