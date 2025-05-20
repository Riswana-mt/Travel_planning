from django.contrib.auth.models import User  
from django.db import models
from django.conf import settings  
import random
from django.urls import reverse





class PhoneOTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    def generate_otp(self):
        # Generate 6-digit OTP
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('beach', 'Beach'),
        ('outdoor', 'Outdoor'),
        ('relax', 'Relax'),
        ('romance', 'Romance'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='place_pic/', blank=True, null=True)
    km = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    

# for review model



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    location = models.CharField(max_length=100)  # Or link to your Location model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})