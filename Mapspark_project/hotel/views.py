
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .models import Destination, Itinerary, Budget, PackingItem
from .forms import DestinationForm, ItineraryForm, BudgetForm, PackingItemForm
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
#from .models import HotelBooking
from django.contrib import messages
#from datetime import date, datetime, time
from django.http import Http404
from django.views.decorators.cache import never_cache
from .models import Booking 




#Travel Planning views

@login_required
@never_cache
def travel_plan(request):
    return render(request,"travel_plan.html")


@login_required
@never_cache
def dashboard(request):
    destinations = Destination.objects.filter(user=request.user)
    itineraries = Itinerary.objects.filter(user=request.user).order_by('date')[:5]
    budgets = Budget.objects.filter(user=request.user)
    
    # Calculate total budget information
    total_budget = sum(b.total_budget for b in budgets)
    total_spent = sum(b.accommodation + b.transportation + b.food + b.activities for b in budgets)
    
    context = {
        'destinations': destinations,
        'itineraries': itineraries,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining': total_budget - total_spent,
    }
    return render(request, 'dashboard.html', context)




@login_required
@never_cache
def destinations(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user
            destination.save()
            messages.success(request, 'Destination added successfully!')
            return redirect('destinations')
    else:
        form = DestinationForm()
    
    destinations = Destination.objects.filter(user=request.user)
    return render(request, 'destinations.html', {
        'form': form,
        'destinations': destinations,
    })

@login_required
@never_cache
def itinerary(request, destination_id=None):
    if request.method == 'POST':
        form = ItineraryForm(request.user, request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.save()
            messages.success(request, 'Itinerary item added!')
            return redirect('itinerary')
    else:
        form = ItineraryForm(request.user)
    
    itineraries = Itinerary.objects.filter(user=request.user)
    if destination_id:
        itineraries = itineraries.filter(destination_id=destination_id)
    
    return render(request, 'itinerary.html', {
        'form': form,
        'itineraries': itineraries.order_by('date'),
    })



@login_required
@never_cache
def budget(request, destination_id=None):
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget added!')
            return redirect('budget')
    else:
        form = BudgetForm(request.user)
    
    budgets = Budget.objects.filter(user=request.user)
    if destination_id:
        budgets = budgets.filter(destination_id=destination_id)
    
    return render(request, 'budget.html', {
        'form': form,
        'budgets': budgets,
    })

@login_required
@never_cache
def packing_list(request, destination_id=None):
    if request.method == 'POST':
        form = PackingItemForm(request.user, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Item added to packing list!')
            return redirect('packing-list')
    else:
        form = PackingItemForm(request.user)
    
    items = PackingItem.objects.filter(user=request.user)
    if destination_id:
        items = items.filter(destination_id=destination_id)
    
    categories = dict(PackingItem.CATEGORIES)
    return render(request, 'packing_list.html', {
        'form': form,
        'items': items,
        'categories': categories,
    })



@login_required
@never_cache
def download_full_itinerary_pdf(request):
    user = request.user
    destinations = Destination.objects.filter(user=user)
    itineraries = Itinerary.objects.filter(user=user)
    budgets = Budget.objects.filter(user=user)
    packing_items = PackingItem.objects.filter(user=user)

    template_path = 'smart_itinerary_pdf.html'
    context = {
        'destinations': destinations,
        'itineraries': itineraries,
        'budgets': budgets,
        'packing_items': packing_items,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="smart_itinerary.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response


@login_required
@never_cache
def toggle_packed(request, item_id):
    item = get_object_or_404(PackingItem, id=item_id, user=request.user)
    item.is_packed = not item.is_packed
    item.save()
    return redirect('packing-list')

@login_required
@never_cache
def delete_item(request, model_name, item_id):
    models = {
        'destination': Destination,
        'itinerary': Itinerary,
        'budget': Budget,
        'packingitem': PackingItem,
    }
    
    model = models.get(model_name.lower())
    if not model:
        messages.error(request, 'Invalid item type')
        return redirect('dashboard')
    
    item = get_object_or_404(model, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Item deleted successfully')
    
    if model_name == 'destination':
        return redirect('destinations')
    elif model_name == 'itinerary':
        return redirect('itinerary')
    elif model_name == 'budget':
        return redirect('budget')
    elif model_name == 'packingitem':
        return redirect('packing-list')
    








@login_required
#def hotel_detail(request, pk):
   # hotel = get_object_or_404(Hotel, pk=pk, destination__user=request.user)
    #return render(request, 'travel_app/hotel_detail.html', {'hotel': hotel})

@login_required
def toggle_booked(request, pk):
    #hotel = get_object_or_404(Hotel, pk=pk, destination__user=request.user)
   #hotel.is_booked = not hotel.is_booked
    #hotel.save()
    return redirect('hotel-detail', pk=pk)


@login_required
@never_cache
def delete_item(request, model_name, item_id):
    models = {
        'destination': Destination,
        'itinerary': Itinerary,
        'budget': Budget,
        'packingitem': PackingItem,
       
    }
    
    model = models.get(model_name.lower())
    if not model:
        messages.error(request, 'Invalid item type')
        return redirect('dashboard')
    
    item = get_object_or_404(model, id=item_id)
    
    
    if hasattr(item, 'user'):
        if item.user != request.user:
            raise PermissionDenied
    elif hasattr(item, 'destination'):
        if item.destination.user != request.user:
            raise PermissionDenied
    
    item.delete()
    messages.success(request, 'Item deleted successfully')
    
    redirect_urls = {
        'destination': 'destinations',
        'itinerary': 'itinerary',
        'budget': 'budget',
        'packingitem': 'packing-list',
        'hotel': 'hotels',
    }
    
    return redirect(redirect_urls.get(model_name.lower(), 'dashboard'))



#for hotel adding views

def home(request):
    return render(request, 'home.html')



#from django.views.decorators.csrf import csrf_exempt

# Mock database
MOCK_HOTELS = {
    "usa": [
        {"name": "Grand Hyatt", "address": "New York", "price": 200},
        {"name": "Motel 6", "address": "Los Angeles", "price": 50}
    ],
    "france": [
        {"name": "Le Ritz Paris", "address": "Paris", "price": 500}
    ]
}


@login_required
def hotel_buk(request):
    return render(request,"hotel_buk.html")


@login_required
def search_hotels(request):
    if request.method == 'GET':
        country = request.GET.get('country', '').lower()
        hotels = MOCK_HOTELS.get(country, [])
        return render(request, 'hotel_buk.html', {'hotels': hotels})
    return redirect('hotel_buk')


@login_required
def booking(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        address = request.GET.get('address', '')
        price = request.GET.get('price', '')
        return render(request,'booking.html', {
            'name': name,
            'address': address,
            'price': price
        })
    return redirect('hotel_buk')






@login_required
def hotel_booking(request):
    if request.method == 'POST':
        
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        guests = request.POST.get('guests')
        
       
        booking = Booking.objects.create(
            hotel_name=request.GET.get('name'),
            user=request.user if request.user.is_authenticated else None,
            checkin_date=checkin,
            checkout_date=checkout,
            guests=guests,
            price=request.GET.get('price'),
            payment_status='Completed'  
        )
        
        messages.success(request, "Booking confirmed! Thank you.")
        return redirect('booking_confirmation', booking_id=booking.id)
    
    # GET request: Show booking form with PayPal button
    hotel_data = {
        'name': request.GET.get('name'),
        'price': request.GET.get('price'),
        
    }
    return render(request, 'booking.html', {'hotel': hotel_data})




@login_required
def booking_confirmation(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        return render(request, 'confirmation.html', {
            'booking': booking
        })
    except Booking.DoesNotExist:
        raise Http404("Booking not found")
    


@login_required
def process_booking(request):
    if request.method == 'POST':
        # Verify PayPal payment
        paypal_order_id = request.POST.get('paypal_order_id')
        # Add your verification logic here
        
        # Process booking
        booking = Booking.objects.create(
            user=request.user,
            hotel_name=request.session.get('hotel_name'),
            price=request.session.get('price'),
            paypal_order_id=paypal_order_id,
            status='completed'
        )
        return redirect('confirmation', booking_id=booking.id)


@login_required
def success(request):
    return render(request, 'success.html')

@login_required
def results(request):
    return render(request,"results.html")


