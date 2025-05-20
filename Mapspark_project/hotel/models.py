from django.db import models
from django.conf import settings  # Import settings for AUTH_USER_MODEL
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User




class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


# Travel planning models
class Destination(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    best_time_to_visit = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('destination-detail', kwargs={'pk': self.pk})

class Itinerary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    activities = models.TextField()
    
    def __str__(self):
        return f"{self.title} - {self.date}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    accommodation = models.DecimalField(max_digits=10, decimal_places=2)
    transportation = models.DecimalField(max_digits=10, decimal_places=2)
    food = models.DecimalField(max_digits=10, decimal_places=2)
    activities = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    
    def remaining_budget(self):
        spent = self.accommodation + self.transportation + self.food + self.activities
        return self.total_budget - spent

class PackingItem(models.Model):
    CATEGORIES = [
        ('CL', 'Clothing'),
        ('TO', 'Toiletries'),
        ('EL', 'Electronics'),
        ('DO', 'Documents'),
        ('OT', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    is_packed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



#Hotel,Booking

class HotelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    city_code = models.CharField(max_length=10)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    offer_id = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel_name} - {self.user.username}"
    




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hotel_name = models.CharField(max_length=200)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    guests = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.hotel_name}"