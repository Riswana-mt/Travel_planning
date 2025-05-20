
from django.urls import path
from core_app import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.shortcuts import redirect

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home') 

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('about/',views.about,name="about"),
    path('base/',views.base,name="base"),
    path('footer/',views.footer,name="footer"),
    path('logout/', logout_view, name='logout'),

    #Email otp urls 
    path('otp/request/', views.otp_request_view, name='otp_request'),
    path('otp/verify/', views.otp_verify_view, name='otp_verify'),
    path('otp/resend/', views.otp_resend_view, name='otp_resend'),

    #Hotel API urls
    path('api/city-code/', views.get_city_code, name='city_code'),
    path('api/search-hotels/', views.search_hotels, name='search_hotels'),
    path('results/', views.search_results, name='search_results'),
    path('get-place',views.get_places_by_category,name='get-places'),
    #path('index2',views.index2,name="index2"),
    path('index/',views.index,name="index"),
    path('account/login/',views.login_view,name="login"), 
    path('signup/',views.signup,name="signup"),
   
    path('login/', views.login_view, name='login'),
   # path('logout/',views.custom_logout, name='logout'),
    # review urls 
    path('review', views.review_list, name='review-list'),
    path('create/', views.review_create, name='review-create'),
    path('<int:pk>/', views.review_detail, name='review-detail'),
    path('<int:pk>/update/', views.review_update, name='review-update'),
    path('<int:pk>/delete/', views.review_delete, name='review-delete'),
      

]