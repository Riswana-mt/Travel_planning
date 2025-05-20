
# Create your views here.
from django.shortcuts import render
from .amadeus_client import search_flights
from django.contrib.auth.decorators import login_required


@login_required
def flight_search_view(request):
    flights = []
    error = None

    if request.method == "POST":
        origin = request.POST.get("origin").upper()
        destination = request.POST.get("destination").upper()
        date = request.POST.get("date")

        flights = search_flights(origin, destination, date)
        if "error" in flights:
            error = flights["error"]

    return render(request, "flight_search.html", {"flights": flights, "error": error})

@login_required
def check_out(request):
    return render(request,"check_out.html")

@login_required
def base(request):
    return render(request,"base.html")

@login_required
def payment_success(request):
    return render(request,"payment_success.html")

@login_required
def traveller_info(request):
    return render(request,"traveller_info.html")

@login_required
def payment(request):
    return render(request,"payment.html")

@login_required
def confirmation(request):
    return render(request,"confirmation.html")
