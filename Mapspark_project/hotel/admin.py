from django.contrib import admin

# Register your models here.


from .models import PackingItem,Budget,Itinerary,Destination

admin.site.register(PackingItem)
admin.site.register(Budget)
admin.site.register(Itinerary)
admin.site.register(Destination)



class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'star_rating', 'price_per_night', 'is_booked')
    list_filter = ('star_rating', 'is_booked', 'destination')
    search_fields = ('name', 'destination__name')
