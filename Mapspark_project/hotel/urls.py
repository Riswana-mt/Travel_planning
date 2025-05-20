from django.urls import path
from . import views

urlpatterns = [
    path('travel_plan/',views.travel_plan,name="travel_plan"),
   # path('dashb/', views.dashboard, name='dashboard'),
    path('destinations/', views.destinations, name='destinations'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('itinerary/<int:destination_id>/', views.itinerary, name='itinerary-destination'),
    path('budget/', views.budget, name='budget'),
    path('budget/<int:destination_id>/', views.budget, name='budget-destination'),
    path('packing-list/', views.packing_list, name='packing-list'),
    path('packing-list/<int:destination_id>/', views.packing_list, name='packing-list-destination'),
    path('toggle-packed/<int:item_id>/', views.toggle_packed, name='toggle-packed'),
    path('delete/<str:model_name>/<int:item_id>/', views.delete_item, name='delete-item'),
    path('smart-itinerary/download/', views.download_full_itinerary_pdf, name='download_full_itinerary_pdf'),

  

    # Authentication URLs
    path('hotel_buk/',views.hotel_buk,name='hotel_buk'),
    path('search/', views.search_hotels, name='search'),
    path('booking/', views.booking, name='booking'),
    path('success/', views.success, name='success'),
    path('results/',views.results,name="results"),
    path('hotel_buk/booking/', views.hotel_booking, name='hotel_booking'),
     path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    


]
    


   



