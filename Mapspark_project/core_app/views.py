from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
import random
from .models import Place
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login, get_user_model
import os
import requests
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.core.cache import cache
import string
from django.views.decorators.csrf import csrf_exempt
from .models import Review
from .forms import ReviewForm
from django.views.decorators.cache import never_cache

# Create your views here.

#Dashboard View
@never_cache
@login_required
def dashboard(request):
   
    return render(request, 'dashboard.html', {
        'user': request.user,
        'first_name': request.user.first_name or request.user.username
    })


#Homepage View
def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'home.html')


#Profile view

@login_required
@never_cache
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'google_account': user.socialaccount_set.filter(provider='google').first()
    }
    return render(request, 'profile.html', context)



#Email otp send View
def send_otp_email(email, otp_code):
    context = {'otp': otp_code}
    email_body = render_to_string('otp_email.html', context)

    try:
        send_mail(
            subject='Your OTP Code for MapSpark',
            message='',  
            from_email='no-reply@mapspark.com',
            recipient_list=[email],
            fail_silently=False,
            html_message=email_body
        )
    except Exception as e:
        print(f"Failed to send OTP email: {str(e)}")
        raise



#Email otp request view

@require_POST
def otp_request_view(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)
    
    # Generate 6-digit OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    cache.set(f'otp_{email}', otp, timeout=300)  # 5 minutes
    
    # Send OTP via email
    try:
        send_otp_email(email, otp)
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return JsonResponse({'error': 'Failed to send OTP'}, status=500)
    
    return JsonResponse({'success': True})


# email otp verify view

@require_POST
def otp_verify_view(request):
    email = request.POST.get('email')
    user_otp = ''.join([
        request.POST.get('otp_1', ''),
        request.POST.get('otp_2', ''),
        request.POST.get('otp_3', ''),
        request.POST.get('otp_4', ''),
        request.POST.get('otp_5', ''),
        request.POST.get('otp_6', '')
    ])
    
    stored_otp = cache.get(f'otp_{email}')
    
    if not stored_otp or user_otp != stored_otp:
        return JsonResponse({'error': 'Invalid OTP'}, status=400)
    
    User = get_user_model()
    
    
    username = email.split('@')[0]
    
    
    while User.objects.filter(username=username).exists():
        username = f"{email.split('@')[0]}_{random.randint(100, 999)}"
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            
        }
    )
    
    login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
    cache.delete(f'otp_{email}')
    return JsonResponse({
        'success': True,
        'redirect_url': '/index/'
    })


# email otp resend view
@require_POST
def otp_resend_view(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)
    
    # Generate new OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    cache.set(f'otp_{email}', otp, timeout=300)
    
    
    print(f"New OTP for {email}: {otp}")  
    
    return JsonResponse({'success': True})



# login Admin & agency

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role in ['admin', 'agency']:  
                auth_login(request, user)
                
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'agency':
                    return redirect('agency_dashboard')
            else:
                messages.error(request, "Access denied for regular users")
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')



#logout view

#def custom_logout(request):
  #  logout(request)
  #  return redirect('/')




# landing page
@login_required
@never_cache
def index(request):
    return render(request,"index.html")
# signup
def signup(request):
    return render(request,"signup.html")

@never_cache
def about(request):
    return render(request,"about.html")
def base(request):
    return render(request,"base.html")

def footer(request):
    return render(request,"footer.html")



# Index page Category wise placesview

def get_places_by_category(request):
    category = request.GET.get('category')
    places = Place.objects.filter(category=category)
    return render(request, 'partials/place_list.html', {'places': places})



# hotel API calling views

load_dotenv()

AMADEUS_API_KEY = os.getenv('w0yYmf9UnZG2kkDw0GWzGJPppy9g27lj')

def get_city_code(request):
    city = request.GET.get('city')
    url = f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY&keyword={city}"
    
    headers = {'Authorization': f'Bearer {AMADEUS_API_KEY}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return JsonResponse(response.json())
    return JsonResponse({'error': 'City not found'}, status=400)

def search_hotels(request):
    city_code = request.GET.get('city_code')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    
    url = f"https://test.api.amadeus.com/v1/shopping/hotel-offers?cityCode={city_code}&checkInDate={checkin}&checkOutDate={checkout}"
    headers = {'Authorization': f'Bearer {AMADEUS_API_KEY}'}
    
    response = requests.get(url, headers=headers)
    return JsonResponse(response.json())


def search_results(request):
    if request.method == 'GET':
        
        destination = request.GET.get('destination')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')
        
        context = {
            'destination': destination,
            'checkin': checkin,
            'checkout': checkout
        }
        return render(request,'results.html', context)
    

# for review page 

@login_required
@never_cache
def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review_detail.html', {'review': review})

@login_required
@never_cache
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been created!')
            return redirect('review-detail', pk=review.pk)
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form})

@login_required
@never_cache
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, "You can't edit this review.")
        return redirect('review-list')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('review-detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_form.html', {'form': form})

@login_required
@never_cache
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, "You can't delete this review.")
        return redirect('review-list')
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted!')
        return redirect('review-list')
    
    return render(request, 'review_confirm_delete.html', {'review': review})
